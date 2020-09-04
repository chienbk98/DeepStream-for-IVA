import sys
sys.path.append('../')
import gi
import configparser
gi.require_version("Gst", '1.0')
from gi.repository import GObject, Gst
from gi.repository import GLib
from ctypes import *
import time
import sys
import math
import platform
from common.is_aarch_64 import is_aarch64
from common.bus_call import bus_call
from common.FPS import GETFPS
import numpy as np
import pyds
import cv2
import os
import os.path
from os import path
from datetime import datetime

import myLib
import myUI
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = "dummy"

MUXER_OUTPUT_WIDTH=1920
MUXER_OUTPUT_HEIGHT=1080
MUXER_BATCH_TIMEOUT_USEC=4000000
TILED_OUTPUT_WIDTH=1920
TILED_OUTPUT_HEIGHT=1080
GST_CAPS_FEATURES_NVMM="memory:NVMM"
pgie_classes_str= ["Person"]
object_name = {0: "person"}


file_config_nvinfer = "/opt/nvidia/deepstream/deepstream-5.0/sources/python/apps/deepstream-imagedata-multistream/Model_Yolo/config_infer_primary_yoloV3.txt"
file_config_tracker = 'dstest2_tracker_config.txt'

list_IP = ["rtsp://192.168.1.9:43794"]
number_sources = len(list_IP)
def cb_newpad(decodebin, decoder_src_pad,data):
    print("In cb_newpad\n")
    caps=decoder_src_pad.get_current_caps()
    gststruct=caps.get_structure(0)
    gstname=gststruct.get_name()
    source_bin=data
    features=caps.get_features(0)

    # Need to check if the pad created by the decodebin is for video and not
    # audio.
    if(gstname.find("video")!=-1):
        # Link the decodebin pad only if decodebin has picked nvidia
        # decoder plugin nvdec_*. We do this by checking if the pad caps contain
        # NVMM memory features.
        if features.contains("memory:NVMM"):
            # Get the source bin ghost pad
            bin_ghost_pad=source_bin.get_static_pad("src")
            if not bin_ghost_pad.set_target(decoder_src_pad):
                sys.stderr.write("Failed to link decoder src pad to source bin ghost pad\n")
        else:
            sys.stderr.write(" Error: Decodebin did not pick nvidia decoder plugin.\n")

def decodebin_child_added(child_proxy,Object,name,user_data):
    print("Decodebin child added:", name, "\n")
    if(name.find("decodebin") != -1):
        Object.connect("child-added",decodebin_child_added,user_data)   
    if(is_aarch64() and name.find("nvv4l2decoder") != -1):
        print("Seting bufapi_version\n")
        Object.set_property("bufapi-version",True)

def create_source_bin(index,uri):
    print("Creating source bin")

    # Create a source GstBin to abstract this bin's content from the rest of the
    # pipeline
    bin_name="source-bin-%02d" %index
    print(bin_name)
    nbin=Gst.Bin.new(bin_name)
    if not nbin:
        sys.stderr.write(" Unable to create source bin \n")

    # Source element for reading from the uri.
    # We will use decodebin and let it figure out the container format of the
    # stream and the codec and plug the appropriate demux and decode plugins.
    uri_decode_bin=Gst.ElementFactory.make("uridecodebin", "uri-decode-bin")
    if not uri_decode_bin:
        sys.stderr.write(" Unable to create uri decode bin \n")
    # We set the input uri to the source element
    uri_decode_bin.set_property("uri",uri)
    # Connect to the "pad-added" signal of the decodebin which generates a
    # callback once a new pad for raw data has beed created by the decodebin
    uri_decode_bin.connect("pad-added",cb_newpad,nbin)
    uri_decode_bin.connect("child-added",decodebin_child_added,nbin)

    # We need to create a ghost pad for the source bin which will act as a proxy
    # for the video decoder src pad. The ghost pad will not have a target right
    # now. Once the decode bin creates the video decoder and generates the
    # cb_newpad callback, we will set the ghost pad target to the video decoder
    # src pad.
    Gst.Bin.add(nbin,uri_decode_bin)
    bin_pad=nbin.add_pad(Gst.GhostPad.new_no_target("src",Gst.PadDirection.SRC))
    if not bin_pad:
        sys.stderr.write(" Failed to add ghost pad in source bin \n")
        return None
    return nbin

def my_sink_pad_buffer_probe(pad, info, u_data):
    '''
    Ham lay du lieu tu sink pad cua element Tiler
    '''
    for arr_point in myLib.center_point:
      myLib.remove_list(arr_point)

    
    gst_buffer = info.get_buffer()
    if not gst_buffer:
        sys.stderr.write("Unable to get GstBuffer")
    batch_meta = pyds.gst_buffer_get_nvds_batch_meta(hash(gst_buffer))
    l_frame = batch_meta.frame_meta_list


    while l_frame is not None:
        try:
            frame_meta = pyds.NvDsFrameMeta.cast(l_frame.data)
        except StopIteration:
            break

        n_frame = pyds.get_nvds_buf_surface(hash(gst_buffer), frame_meta.batch_id)
        frame_image = np.array(n_frame, copy=True, order='C')
        frame_image = myLib.rgba2rgb(frame_image)

        # Lay ra GList Object trong frame
        l_obj = frame_meta.obj_meta_list

        while l_obj is not None:
            try: # Chuyen GList sang sang metadata la NvDsObjectMeta
                obj_meta = pyds.NvDsObjectMeta.cast(l_obj.data)
            except StopIteration:
                break
            frame_image=myLib.draw_bounding_boxes(image=frame_image,obj_meta=obj_meta,track_id=obj_meta.object_id,source_id=frame_meta.batch_id)
            print("Frame Number: {}, Num object in frame: {}, Object_name: {}, Object_ID: {}, Confidence {}, Source_ID: {}"
            .format(frame_meta.frame_num ,frame_meta.num_obj_meta, object_name[obj_meta.class_id], obj_meta.object_id, obj_meta.confidence, frame_meta.batch_id))
            try:
                l_obj = l_obj.next
            except StopIteration:
                break

        myUI.image_result = [frame_image] * 3

        try:
            l_frame = l_frame.next
        except StopIteration:
            break
    # print("=====================================")
    return Gst.PadProbeReturn.OK

class PipeLine():
    def __init__(self, tracking = True, on_screen_display = False):
        '''
        tracking: use tracker
        on_screen_display: su dung element hien thi cua Deepstream
        '''
        GObject.threads_init()
        Gst.init(None)
        print("Creating Pipeline \n ")
        self.tracking = tracking
        self.on_screen_display = on_screen_display
        self.pipeline = Gst.Pipeline()
        self.createElement()
        self.configElements()
        self.addingAndLinkingElements()
        self.getBuffer()

    def createElement(self):
        print("Creating the elements")
        self.streammux = Gst.ElementFactory.make("nvstreammux", "Stream-muxer")
        self.pipeline.add(self.streammux)

        for i in range(number_sources):
            print("Creating source_bin ",i," \n ")
            uri_name=list_IP[i]
            if uri_name.find("rtsp://") == 0 :
                is_live = True
            source_bin=create_source_bin(i, uri_name)
            if not source_bin:
                sys.stderr.write("Unable to create source bin \n")
            self.pipeline.add(source_bin)
            padname="sink_%u" %i
            sinkpad= self.streammux.get_request_pad(padname) 
            if not sinkpad:
                sys.stderr.write("Unable to create sink pad bin \n")
            srcpad=source_bin.get_static_pad("src")
            if not srcpad:
                sys.stderr.write("Unable to create src pad bin \n")
            srcpad.link(sinkpad)


        self.pgie = Gst.ElementFactory.make("nvinfer", "primary-inference")
        self.nvvidconv1 = Gst.ElementFactory.make("nvvideoconvert", "convertor1")
        caps1 = Gst.Caps.from_string("video/x-raw(memory:NVMM), format=RGBA")
        self.filter1 = Gst.ElementFactory.make("capsfilter", "filter1")
        self.filter1.set_property("caps", caps1)
        self.tiler=Gst.ElementFactory.make("nvmultistreamtiler", "nvtiler")
        self.nvvidconv = Gst.ElementFactory.make("nvvideoconvert", "convertor")
        self.nvosd = Gst.ElementFactory.make("nvdsosd", "onscreendisplay")
        if(is_aarch64()):
            print("Creating transform \n ")
            if self.on_screen_display:
              self.transform=Gst.ElementFactory.make("nvegltransform", "nvegl-transform")
            else:
              self.transform=Gst.ElementFactory.make("queue", "nvegl-transform")
        if not self.transform:
            sys.stderr.write(" Unable to create transform \n")
    
        if self.on_screen_display:
          self.sink = Gst.ElementFactory.make("nveglglessink", "nvvideo-renderer")
        else:
          self.sink = Gst.ElementFactory.make("fakesink", "nvvideo-renderer")
        
        if is_live:
            print("Atleast one of the sources is live")
            self.streammux.set_property('live-source', 1)
        if self.tracking:
          print("Create Tracker Element")
          self.tracker = Gst.ElementFactory.make("nvtracker", "tracker")
          self.pipeline.add(self.tracker)

    def configElements(self):
        self.streammux.set_property('width', MUXER_OUTPUT_WIDTH)
        self.streammux.set_property('height', MUXER_OUTPUT_HEIGHT)
        self.streammux.set_property('batch-size', number_sources)
        self.streammux.set_property('batched-push-timeout', MUXER_BATCH_TIMEOUT_USEC)#4000000)

        self.pgie.set_property('config-file-path', file_config_nvinfer)




        pgie_batch_size=self.pgie.get_property("batch-size")
        if(pgie_batch_size != number_sources):
            print("WARNING: Overriding infer-config batch-size",pgie_batch_size," with number of sources ", number_sources," \n")
            self.pgie.set_property("batch-size",number_sources)
        tiler_rows=int(math.sqrt(number_sources))
        tiler_columns=int(math.ceil((1.0*number_sources)/tiler_rows))
        self.tiler.set_property("rows",tiler_rows)
        self.tiler.set_property("columns",tiler_columns)
        self.tiler.set_property("width", TILED_OUTPUT_WIDTH)
        self.tiler.set_property("height", TILED_OUTPUT_HEIGHT)


        if not is_aarch64():
            mem_type = int(pyds.NVBUF_MEM_CUDA_UNIFIED)
            self.streammux.set_property("nvbuf-memory-type", mem_type)
            self.nvvidconv.set_property("nvbuf-memory-type", mem_type)
            self.nvvidconv1.set_property("nvbuf-memory-type", mem_type)
            self.tiler.set_property("nvbuf-memory-type", mem_type)

        if self.tracking:
          config = configparser.ConfigParser()
          config.read(file_config_tracker)
          config.sections()

          for key in config['tracker']:
              if key == 'tracker-width' :
                  tracker_width = config.getint('tracker', key)
                  self.tracker.set_property('tracker-width', tracker_width)
              if key == 'tracker-height' :
                  tracker_height = config.getint('tracker', key)
                  self.tracker.set_property('tracker-height', tracker_height)
              if key == 'gpu-id' :
                  tracker_gpu_id = config.getint('tracker', key)
                  self.tracker.set_property('gpu_id', tracker_gpu_id)
              if key == 'll-lib-file' :
                  tracker_ll_lib_file = config.get('tracker', key)
                  self.tracker.set_property('ll-lib-file', tracker_ll_lib_file)
              if key == 'll-config-file' :
                  tracker_ll_config_file = config.get('tracker', key)
                  self.tracker.set_property('ll-config-file', tracker_ll_config_file)
              if key == 'enable-batch-process' :
                  tracker_enable_batch_process = config.getint('tracker', key)
                  self.tracker.set_property('enable_batch_process', tracker_enable_batch_process)
        
    def addingAndLinkingElements(self):
        print("Adding elements to Pipeline \n")
        self.pipeline.add(self.pgie)
        self.pipeline.add(self.tiler)
        self.pipeline.add(self.nvvidconv)
        self.pipeline.add(self.filter1)
        self.pipeline.add(self.nvvidconv1)
        self.pipeline.add(self.nvosd)
        if is_aarch64():
            self.pipeline.add(self.transform)
        self.pipeline.add(self.sink)

        print("Linking elements in the Pipeline \n")
        self.streammux.link(self.pgie)    
        self.pgie.link(self.tracker)
        self.tracker.link(self.nvvidconv1)
        self.nvvidconv1.link(self.filter1)
        self.filter1.link(self.tiler)
        self.tiler.link(self.nvvidconv)
        self.nvvidconv.link(self.nvosd)
        if is_aarch64():
            self.nvosd.link(self.transform)
            self.transform.link(self.sink)
        else:
            self.nvosd.link(self.sink)
    
    def getBuffer(self):
        self.loop = GObject.MainLoop()
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect ("message", bus_call, self.loop)

        tiler_sink_pad=self.tiler.get_static_pad("sink")
        if not tiler_sink_pad:
            sys.stderr.write(" Unable to get src pad \n")
        else:
            tiler_sink_pad.add_probe(Gst.PadProbeType.BUFFER, my_sink_pad_buffer_probe, 0)
        






if __name__ == '__main__':
    A = PipeLine()
    pipeline = A.pipeline

    print("Starting pipeline \n")
    # start play back and listed to events		
    pipeline.set_state(Gst.State.PLAYING)
    try:
        A.loop.run()
    except:
        pass

    # cleanup
    print("Exiting app\n")
    pipeline.set_state(Gst.State.NULL)