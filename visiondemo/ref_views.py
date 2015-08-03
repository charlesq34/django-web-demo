# Create your views here.
from django.http import HttpResponse
import dbtool
import dbtool2
import dbtoolVerify
import json
import sys
import time
import os
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.clickjacking import xframe_options_exempt
from django.conf import settings
# import matlab.engine
import numpy as np
import random
import string
import glob
import math


@csrf_exempt
@xframe_options_exempt
def testajax(request):
  
  if ('synsetid' not in request.GET) and ('image_synsetid' not in request.GET) and ('gloss' not in request.GET):
    conn = dbtool2.ConnDB()
    #res = dbtool2.Query(conn,'select childid, word from synset_relation_14summer as s join view_synset as v on s.childid=v.synsetid where parentid=82127 and step=0')
    res = dbtool2.Query(conn,'select childid, word from synset_relation_14summer as s join view_synset as v on s.childid=v.synsetid join display_order_14summer as d on s.childid=d.synsetid where parentid=82127 and step=0 order by aligned_num desc,total_num desc')
    num_total = dbtool2.Query(conn,'select count(*) from synset_relation_14summer where parentid=82127')[0][0]
    output = dict()
    output['text'] = "ShapeNet 14summer ("+str(num_total)+")"
    output['li_attr'] = {"synsetid":82127}
    output['state'] = {"opened":1}
    output['children'] = list()
    for r in res:
      tmp = dict()
      num_total = dbtool2.Query(conn,'select count(*) from synset_relation_14summer where parentid=%d'%int(r[0]))[0][0]
      tmp['text'] = r[1]+" ("+str(num_total)+")"
      tmp['li_attr'] = {"synsetid":int(r[0])}
      tmp['state'] = {"opened":0}
      tmp['children'] = True
      output['children'].append(tmp);
    conn.close()
  elif ('image_synsetid' not in request.GET) and ('gloss' not in request.GET):
    synsetid = int(request.GET['synsetid'])
    conn = dbtool2.ConnDB()
    #res = dbtool2.Query(conn,'select childid, word from synset_relation_14summer as s join view_synset as v on s.childid=v.synsetid where parentid=%d and step=0'%synsetid)
    res = dbtool2.Query(conn,'select childid, word from synset_relation_14summer as s join view_synset as v on s.childid=v.synsetid join display_order_14summer as d on s.childid=d.synsetid where parentid=%d and step=0 order by aligned_num desc,total_num desc'%synsetid)
    output = list()
    for r in res:
      tmp = dict()
      num_total = dbtool2.Query(conn,'select count(*) from synset_relation_14summer where parentid=%d'%int(r[0]))[0][0]
      tmp['text'] = r[1]+" ("+str(num_total)+")"
      tmp['li_attr'] = {"synsetid":int(r[0])}
      tmp['state'] = {"opened":0}
      tmp['children'] = True
      output.append(tmp);
    conn.close()
  elif ('gloss' not in request.GET):
    synsetid = int(request.GET['image_synsetid'])
    conn = dbtool2.ConnDB()
    #output = dbtool2.Query(conn,'select imagename,aligned from shapenet_14summer where synsetid=%d or synsetid in (select childid from synset_relation_14summer where parentid=%d) order by intrarank asc limit 1800'%(synsetid,synsetid))
    output = dbtool2.Query(conn,'select imagename,aligned from shapenet_14summer where synsetid=%d order by intrarank asc limit 1800'%synsetid)
    conn.close()
  else:
    synsetid = int(request.GET['gloss'])
    conn = dbtool2.ConnDB()
    output = dbtool2.Query(conn,'select word,gloss from view_synset where synsetid=%d'%synsetid)[0]
    conn.close()

  return HttpResponse(json.dumps(output),mimetype='application/json')


def shapenet(request):
    html = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link rel="stylesheet" href="../../media/www/internal/files/Test/files/layout-default-latest.css" />
<link href="../../media/www/internal/files/Test/files/bootstrap.min.css" rel="stylesheet"/>
<link rel="stylesheet" href="../../media/www/internal/files/Test/files/jumbotron-narrow.css" />
<link rel="stylesheet" href="../../media/www/internal/files/Test/files/jstree/themes/default/style.min.css" />
<link rel="stylesheet" href="../../media/www/internal/files/Test/files/css.css" />
<link rel="stylesheet" href="../../media/www/internal/files/Test/files/image-explore.css" />
<link rel="stylesheet" href="../../media/www/internal/files/Test/files/lightbox/css/lightbox.css" />
<link rel="shortcut icon" href="../../media/www/internal/files/Test/shapeNet.ico">

<script src="../../media/www/internal/files/Test/files/jquery.layout-latest.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.3/jquery-ui.min.js"></script>
<script src="../../media/www/internal/files/Test/files/jquery.pagination.js"></script>
<script src="../../media/www/internal/files/Test/files/jstree/jstree.min.js"></script>
<script src="../../media/www/internal/files/Test/files/lightbox/js/lightbox-2.6.min.js"></script>
<script src="../../media/www/internal/files/Test/files/js.js"></script>
<title>ShapeNet</title>
</head>

<body class="" style="dmargin: 20px;">

<div class="navbar navbar-default navbar-fixed-top" role="navigation" style="background:#FFF; border-width:medium">
  <div class="container">
  <a class="" href="#"><img src="../../media/www/internal/files/Test/logo.png"  width="600" height="55" style="padding:0px 0px 0px 0px; margin-top:8px;"/></a>
    <div class="navbar-header">
      <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <!-- a class="navbar-band" -->
          </div>
    <div class="collapse navbar-collapse">
          <ul class="nav navbar-nav" style="height:40px;">
            <li ><a href="#">Home</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
            <!--<li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown">Dropdown <b class="caret"></b></a>
              <ul class="dropdown-menu">
                <li><a href="#">Action</a></li>
                <li><a href="#">Another action</a></li>
                <li><a href="#">Something else here</a></li>
                <li class="divider"></li>
                <li class="dropdown-header">Nav header</li>
                <li><a href="#">Separated link</a></li>
                <li><a href="#">One more separated link</a></li>
              </ul>
            </li>-->
          </ul>
        </div>
  </div>
</div>
<br/>
<br/>
<br/>
<br/>
<br/>

<div class="container" style="margin-top: 20px; border-radius:6px">
<div class="well" id="headline"><font size="4">&nbsp&nbsp</font><br>&nbsp&nbsp</div>
<div class="jumbotron ui-layout-container" style="overflow:hidden; postion:relative">
  <div id="container" class="row-marketing">
    <div id="tree1" class="col-xs-4">

      <div id="tree-2">
      </div>

      <!--div id="jstree1" class="demo">
        <ul>
          <li>Root node 1
          <ul>
            <li><a href="#"><em>initially</em> <strong>selected</strong></a></li>
            <li>custom icon URL</li>
            <li>initially open
            <ul>
              <li>Another node</li>
            </ul>
            </li>
            <li data-jstree='{ "icon" : "glyphicon glyphicon-leaf" }'>Custom icon class (bootstrap)</li>
          </ul>
          </li>
          <li><a href="http://www.jstree.com">Root node 2</a></li>
        </ul>
      </div-->

    </div>

    <div id="" class="col-xs-8">

      <div id="panel" class="ui-tabs-panel ui-widget-content ui-corner-bottom">
        <div id="imagespanel"><ul></ul></div>
        <div id="pagination"></div>
      </div>
    </div>

  </div>
 </div>
</div>
<br>
<br>
<br>

</body>
</html>'''
    return HttpResponse(html)

@xframe_options_exempt
def anno(request):
    try:
      taskid = int(request.GET['taskid'])
      conn = dbtool2.ConnDB()
#new
      tic = time.clock()
      res1 = dbtool2.Query(conn, 'select synsetid, targetsynsetid,imageid from bbox_taskset where taskid=%d'%taskid)
      img_cur = list()
      img_smp = list()
      for r1 in res1:
	tmp = dbtool2.Query(conn, 'select imageid, imagename from all_image2 as i join bbox_request_record2 as r using (synsetid) where r.synsetid=%d and r.targetsynsetid=%d and i.imageid=%d' % (r1[0],r1[1],r1[2]))
	img_cur.append({'imageid':tmp[0][0], 'imagedirectory':'/'.join([tmp[0][1][i:i+1] for i in range(0, 5)])+'/'+tmp[0][1][5:len(tmp[0][1])]+'/'+tmp[0][1], 'imagename':tmp[0][1]})
      toc = time.clock()
      conn.close()
      print '********************', toc-tic, '*********************'
#old
      #res = dbtool2.Query(conn, 'select imageid, imagename from bbox_taskset join all_image using(synsetid, targetsynsetid, imageid) where taskid=%d' % taskid)
      conn = dbtool2.ConnDB()
      synsetid,synsetword,gloss = dbtool2.Query(conn,'select synsetid, synsetword, gloss from bbox_request_record2 join bbox_task using(synsetid, targetsynsetid) where taskid=%d' % taskid)[0]
      synsetoffset = dbtool2.Query(conn, 'select synsetoffset from view_synset where synsetid=%d'%int(synsetid))
      tg = dbtool2.Query(conn,'select word from word_list join bbox_request_record using(wordid) where synsetid=%d' % int(synsetid))[0][0]
      conn.close()
      conn = dbtool2.ConnDB()
      imagenames = dbtool2.Query(conn, 'select imagename from imagenet_sampleimg where synsetoffset="%s"'%synsetoffset[0])
      #res = dbtool2.Query(conn, 'select imageid, imageurl from bbox_taskset join all_image using(imageid) where taskid=%d' % taskid)
      #img_cur = list()
      #for image in res:
	#img_cur.append({'imageid':image[0], 'imagename':image[1]})
        #img_cur.append({'imageid':image[0], 'imageurl':image[1]})
      conn.close()
      result = dict()
      result['img_cur']=img_cur
      result['tag']=tg
      result['synsetword']=synsetword
      result['synsetoffset']=synsetoffset
      result['gloss']=gloss
      for imagename in imagenames:
          img_smp.append(imagename[0])
      result['img_smp']=img_smp
      output = json.dumps(result)
      html='''<!doctype html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="../../media/www/internal/files/bootstrap.min.css" rel="stylesheet"/>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script src="../../media/www/internal/files/bootstrap.min.js"></script>
<script src="../../media/www/internal/files/js.js"></script>
<script>
var result='''+output+''';
</script>
<title>Annotation</title>
</head>

<body style="dmargin: 0px;">

<div class="container" style="margin-top: 10px; width:1200px;">
<br>
<div class="row-marketing">
<div class="jumbotron ui-layout-container col-xs-8" style="overflow:hidden; postion:relative height:800px; padding-top:20px; padding-bottom:40px; padding-left:40px; padding-right:20px">
<div class="row-marketing">
  <ul class="nav nav-tabs col-xs-4">
    <li class="active"><a href="#home" data-toggle="tab">Home</a></li>
    <li class=""><a href="#wiki" data-toggle="tab">Wikipedia</a></li>
  </ul>
  <div class="col-xs-1">
  </div>
  <div class="well col-xs-7" style=" padding-top:5px; padding-bottom:5px">
    <p style="font-size:14px; margin-bottom:2px"><font color="red"><strong>Instruction</strong></font>: Please pick up models complying with the current definition. Please use the example images as a reference. Click to choose. Double click to cancel. You can also refer to the wikipedia tab. In the event of any contradiction between wiki and the following definition, our definition shall prevail. </p>
  </div>
</div>
<br><br><br>
<div class="row-marketing well" style="overflow:hidden;">
<div>
    <p id="curGloss" style="font-size:16px; font-weight:bold; font-style:border; margin-bottom:2px"></p>
</div>
</div>

  <div class="tab-content">
      <div class="tab-pane active" id="home">
	  <div id="imagespanel">
	    <ul class="col-xs-12">  
	    </ul>
	  </div>
    </div>
  <div class="tab-pane" id="wiki">
    <iframe name="showFrame" id="showFrame" src="" width="100%" height="704px">
    </iframe>
  </div>
</div>
</div>

<div class="col-xs-1" style="overflow:hidden; postion:relative;">
</div>
<div id="selectedpanel" class=" col-xs-3" style="overflow:scroll; postion:relative;height:1952px;background-color:#eee; padding-top:20px; padding-bottom:20px; border-top: 1px solid #e5e5e5; border-bottom: 1px solid #e5e5e5; border-radius:6px;">
<div class="col-xs-12">
</div>
</div>

</div>
</div>
<!--div style="text-align:center; margin-bottom:30px">
<input id="submit" type="button" value="Submit" style="border-radius:3px"></input>-->
<div style="text-align:center; margin-bottom:30px">
<form action="javascript:subresult()">
<input id="submit" type="submit" name="commit1" value="Submit" style="border-radius:3px"></input>
</form>
<form id="mturk_form" action="https://www.mturk.com/mturk/externalSubmit" method="POST"><input type="hidden" id="assignmentId" name="assignmentId" value=""><input type="submit" name="commit2" value="Submit" hidden><input type="hidden" id="num_good" name="num_good" value=""><input id="num_total" type="hidden" name="num_total" value=""></form>
</div>
</body>
</html>
''' 
      return HttpResponse(html)
    except:
      print sys.exc_info()
      return HttpResponse(sys.exc_info())

@csrf_exempt
@xframe_options_exempt
def submit(request):
    if request.method == 'POST':
	correctGoldRatioThreshold = 0.75
        selectedId = request.POST.get('Id')
        selectedId = str(selectedId[1:len(selectedId)-1])

        #fileOut = open('/orions-zfs/projects/haosu/ShapeNet/Code/pycode/django_projects/firstapp/tmp.txt','w')
	#fileOut.writelines(request.method)
	#fileOut.writelines(str(int(request.POST.get('num_total'))))
	#fileOut.writelines(str(int(request.POST.get('num_good'))))
	#fileOut.writelines(str(int(request.POST.get('taskid'))))
	#fileOut.writelines(str(len(selectedId)))
	#fileOut.close()
	    
	taskid = int(request.POST.get('taskid'))
	num_good = int(request.POST.get('num_good'))
	num_total = int(request.POST.get('num_total'))
	if request.POST.get('assignmentId'):
	    amtassignid = str(request.POST.get('assignmentId'))
	    print taskid
	    conn = dbtool2.ConnDB()
            conn.query("insert low_priority ignore into amt_assign (taskid, amtassignid) values (%d,'%s')" % (taskid, amtassignid))
	    assignid = dbtool2.Query(conn, "select assignid from amt_assign where taskid=%d and amtassignid='%s'" % (taskid, amtassignid))[0][0]
	    print assignid
	    conn.query("insert low_priority ignore into bbox_assign (assignid, num_good, num_total) values (%d, %d, %d)" % (assignid, num_good, num_total))
	    res = dbtool2.Query(conn, 'select synsetid, targetsynsetid, imageid from bbox_taskset where taskid=%d' % taskid)
	    for assign in res:
		conn.query("insert low_priority ignore into bbox_answer (assignid, synsetid, targetsynsetid, imageid) values (%d, %d, %d, %d)" % (assignid, assign[0], assign[1], assign[2]))
	    if (len(selectedId)):
                selectedId = selectedId.split(',')
		for sid in selectedId:
		    conn.query("update low_priority bbox_answer set bbox_isgood=1 where assignid=%d and imageid=%d" % (assignid, int(sid)))
	    conn.commit()

	    correctGoldNum = dbtool2.Query(conn,'select count(*) from bbox_image as i join bbox_answer as a using(synsetid,targetsynsetid,imageid) where i.is_gold_seed=1 and a.assignid=%d and a.bbox_isgood=i.isgood'%assignid)[0][0]
	    totalGoldNum = dbtool2.Query(conn,'select count(*) from bbox_image as i join bbox_answer as a using(synsetid,targetsynsetid,imageid) where i.is_gold_seed=1 and a.assignid=%d'%assignid)[0][0]
	    if totalGoldNum==0:
		conn.close()
		return HttpResponse(json.dumps("Thank you!"))
	    else:
	        correctGoldRatio = float(correctGoldNum)/float(totalGoldNum)
	        conn.close()
	        if correctGoldRatio>=correctGoldRatioThreshold:
		    return HttpResponse(json.dumps("Thank you!"))
	        else:
		    return HttpResponse(json.dumps("We found many incorrect annotations in your submission and we cannot approve the assignment!"))
	else:
	    return HttpResponse(json.dumps("Submit without accepting!"))

    else:
        return HttpResponse("Thank you.")

def visres(request):
    taskid = int(request.GET['taskid'])
    conn = dbtool2.ConnDB()
    res1 = dbtool2.Query(conn, 'select synsetid, targetsynsetid,imageid from bbox_taskset where taskid=%d'%taskid)
    synsetword,gloss = dbtool2.Query(conn,'select synsetword, gloss from bbox_request_record2 join bbox_task using(synsetid, targetsynsetid) where taskid=%d' % taskid)[0]
    img_good = list()
    img_med = list()
    img_bad = list()
    for r1 in res1:
	tmp = dbtool2.Query(conn, 'select imageid, imagename from all_image2 as i join bbox_request_record2 as r using (synsetid) where r.synsetid=%d and r.targetsynsetid=%d and i.imageid=%d' % (r1[0],r1[1],r1[2]))
	#if dbtool2.Query(conn,'select count(*) from bbox_image where synsetid=%d and targetsynsetid=%d and imageid=%d and 2*num_bbox_good_vote>=num_bbox_total_vote'%(r1[0],r1[1],r1[2]))[0][0]:
	if dbtool2.Query(conn,'select count(*) from bbox_image where synsetid=%d and targetsynsetid=%d and imageid=%d and num_bbox_good_vote>=2'%(r1[0],r1[1],r1[2]))[0][0]:
	    #img_good.append({'imageid':tmp[0][0], 'imagename':tmp[0][1]})
	    img_good.append({'imageid':tmp[0][0], 'imagedirectory':'/'.join([tmp[0][1][i:i+1] for i in range(0, 5)])+'/'+tmp[0][1][5:len(tmp[0][1])]+'/'+tmp[0][1], 'imagename':tmp[0][1]})
	#elif dbtool2.Query(conn,'select count(*) from bbox_image where synsetid=%d and targetsynsetid=%d and imageid=%d and 2*num_bbox_good_vote<num_bbox_total_vote'%(r1[0],r1[1],r1[2]))[0][0]:
	elif dbtool2.Query(conn,'select count(*) from bbox_image where synsetid=%d and targetsynsetid=%d and imageid=%d and num_bbox_good_vote=0'%(r1[0],r1[1],r1[2]))[0][0]:
	    #img_bad.append({'imageid':tmp[0][0], 'imagename':tmp[0][1]})
	    img_bad.append({'imageid':tmp[0][0], 'imagedirectory':'/'.join([tmp[0][1][i:i+1] for i in range(0, 5)])+'/'+tmp[0][1][5:len(tmp[0][1])]+'/'+tmp[0][1], 'imagename':tmp[0][1]})
	#else:
	#    img_med.append({'imageid':tmp[0][0], 'imagename':tmp[0][1]})
	#if dbtool2.Query(conn,'select count(*) from bbox_image where synsetid=%d and targetsynsetid=%d and imageid=%d and 2*num_bbox_good_vote<num_bbox_total_vote'%(r1[0],r1[1],r1[2]))[0][0]==1 and dbtool2.Query(conn,'select count(*) from bbox_image where synsetid=%d and targetsynsetid=%d and imageid=%d and num_bbox_good_vote>0'%(r1[0],r1[1],r1[2]))[0][0]==1:
	if dbtool2.Query(conn,'select count(*) from bbox_image where synsetid=%d and targetsynsetid=%d and imageid=%d and num_bbox_good_vote=1'%(r1[0],r1[1],r1[2]))[0][0]:
	    #img_med.append({'imageid':tmp[0][0], 'imagename':tmp[0][1]})
	    img_med.append({'imageid':tmp[0][0], 'imagedirectory':'/'.join([tmp[0][1][i:i+1] for i in range(0, 5)])+'/'+tmp[0][1][5:len(tmp[0][1])]+'/'+tmp[0][1], 'imagename':tmp[0][1]})
    result = dict()
    result['img_good']=img_good
    conn.close()
    result['img_bad']=img_bad
    result['img_med']=img_med
    result['synsetword']=synsetword
    result['gloss']=gloss
    output = json.dumps(result)
    html='''<!doctype html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="../../media/www/internal/files/bootstrap.min.css" rel="stylesheet"/>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script src="../../media/www/internal/files/bootstrap.min.js"></script>
<script src="../../media/www/internal/files/js_visres.js"></script>
<script>
var result='''+output+''';
</script>
<title>VisualizeResult</title>
</head>

<body style="dmargin: 0px;">

<div class="container" style="margin-top: 10px; width:1200px;">
<br>
<div class="well" style=" padding-top:5px; padding-bottom:5px" id="synsetword">
</div>

<div class="row-marketing">
<div class="jumbotron ui-layout-container col-xs-5" style="overflow:hidden; postion:relative height:800px; padding-top:20px; padding-bottom:40px; padding-left:40px; padding-right:20px">
  <div>
    <ul class="nav nav-tabs">
      <li class="active"><a data-toggle="tab">Good Images</a></li>
    </ul>
    <ul class="col-xs-12" id="imagegood">  
    </ul>
  </div>
</div>
<div class="jumbotron ui-layout-container col-xs-5" style="overflow:hidden; postion:relative height:800px; padding-top:20px; padding-bottom:40px; padding-left:40px; padding-right:20px">
  <div>
    <ul class="nav nav-tabs">
      <li class="active"><a data-toggle="tab">Bad Images</a></li>
    </ul>
    <ul class="col-xs-12" id="imagebad">  
    </ul>
  </div>
</div>
<div class="jumbotron ui-layout-container col-xs-2" style="overflow:hidden; postion:relative height:800px; padding-top:20px; padding-bottom:40px; padding-left:40px; padding-right:20px">
  <div>
    <ul class="nav nav-tabs">
      <li class="active"><a data-toggle="tab">Not Decided Images</a></li>
    </ul>
    <ul id="imagemed" class="col-xs-12">  
    </ul>
  </div>
</div>
</div>
</div>
</body>
</html>
''' 
    return HttpResponse(html)

def synset(request):
    synsetid = int(request.GET['synsetid'])
    conn = dbtool2.ConnDB()
    res1 = dbtool2.Query(conn, 'select synsetid, targetsynsetid,imageid from bbox_image where synsetid=%d'%synsetid)
    synsetword,gloss = dbtool2.Query(conn,'select synsetword, gloss from bbox_request_record2 where synsetid=%d' % synsetid)[0]
    img_good = list()
    img_med = list()
    img_bad = list()
    for r1 in res1:
	tmp = dbtool2.Query(conn, 'select imageid, imagename from all_image2 as i join bbox_request_record2 as r using (synsetid) where r.synsetid=%d and r.targetsynsetid=%d and i.imageid=%d' % (r1[0],r1[1],r1[2]))
	if dbtool2.Query(conn,'select count(*) from bbox_image where synsetid=%d and targetsynsetid=%d and imageid=%d and num_bbox_good_vote>=2'%(r1[0],r1[1],r1[2]))[0][0]:
	    img_good.append({'imageid':tmp[0][0], 'imagedirectory':'/'.join([tmp[0][1][i:i+1] for i in range(0, 5)])+'/'+tmp[0][1][5:len(tmp[0][1])]+'/'+tmp[0][1], 'imagename':tmp[0][1]})
	elif dbtool2.Query(conn,'select count(*) from bbox_image where synsetid=%d and targetsynsetid=%d and imageid=%d and num_bbox_good_vote=0'%(r1[0],r1[1],r1[2]))[0][0]:
	    img_bad.append({'imageid':tmp[0][0], 'imagedirectory':'/'.join([tmp[0][1][i:i+1] for i in range(0, 5)])+'/'+tmp[0][1][5:len(tmp[0][1])]+'/'+tmp[0][1], 'imagename':tmp[0][1]})
	if dbtool2.Query(conn,'select count(*) from bbox_image where synsetid=%d and targetsynsetid=%d and imageid=%d and num_bbox_good_vote=1'%(r1[0],r1[1],r1[2]))[0][0]:
	    img_med.append({'imageid':tmp[0][0], 'imagedirectory':'/'.join([tmp[0][1][i:i+1] for i in range(0, 5)])+'/'+tmp[0][1][5:len(tmp[0][1])]+'/'+tmp[0][1], 'imagename':tmp[0][1]})
    result = dict()
    result['img_good']=img_good
    conn.close()
    result['img_bad']=img_bad
    result['img_med']=img_med
    result['synsetword']=synsetword
    result['gloss']=gloss
    output = json.dumps(result)

    html='''<!doctype html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="../../media/www/internal/files/bootstrap.min.css" rel="stylesheet"/>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script src="../../media/www/internal/files/bootstrap.min.js"></script>
<script src="../../media/www/internal/files/js_visres.js"></script>
<script>
var result='''+output+''';
</script>
<title>VisualizeResult</title>
</head>

<body style="dmargin: 0px;">

<div class="container" style="margin-top: 10px; width:1200px;">
<br>
<div class="well" style=" padding-top:5px; padding-bottom:5px" id="synsetword">
</div>

<div class="row-marketing">
<div class="jumbotron ui-layout-container col-xs-5" style="overflow:hidden; postion:relative height:800px; padding-top:20px; padding-bottom:40px; padding-left:40px; padding-right:20px">
  <div>
    <ul class="nav nav-tabs">
      <li class="active"><a data-toggle="tab">Good Images</a></li>
    </ul>
    <ul class="col-xs-12" id="imagegood">  
    </ul>
  </div>
</div>
<div class="jumbotron ui-layout-container col-xs-5" style="overflow:hidden; postion:relative height:800px; padding-top:20px; padding-bottom:40px; padding-left:40px; padding-right:20px">
  <div>
    <ul class="nav nav-tabs">
      <li class="active"><a data-toggle="tab">Bad Images</a></li>
    </ul>
    <ul class="col-xs-12" id="imagebad">  
    </ul>
  </div>
</div>
<div class="jumbotron ui-layout-container col-xs-2" style="overflow:hidden; postion:relative height:800px; padding-top:20px; padding-bottom:40px; padding-left:40px; padding-right:20px">
  <div>
    <ul class="nav nav-tabs">
      <li class="active"><a data-toggle="tab">Not Decided Images</a></li>
    </ul>
    <ul id="imagemed" class="col-xs-12">  
    </ul>
  </div>
</div>
</div>
</div>
</body>
</html>
''' 
    return HttpResponse(html)

def index(request):
    html = '''<!doctype html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="../../media/www/internal/files/bootstrap.min.css" rel="stylesheet"/>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script src="../../media/www/internal/files/bootstrap.min.js"></script>
<title>Index</title>
</head>

<body>
<div class="container" style="margin-top: 20px; width:1200px;">
<div class="jumbotron ui-layout-container" style="overflow:hidden; postion:relative height:800px; padding-top:20px; padding-bottom:40px; padding-left:40px; padding-right:20px">
<p><a href="https://shapenet.cs.stanford.edu/">ShapeNet homepage</a></p>
<p><a href="http://shapenet.cs.stanford.edu:8010/model-categorizer.html">Manolis collected models</a></p>
<p><a href="https://shapenet.cs.stanford.edu/internal/stats1?rand=1">Statistics1</a>:an overview of the positive ratio of the 4001 WordNet synsets.(sorted by positive ratio) Please click the synset id to see the annotated results in each synset.</p>
<p><a href="https://shapenet.cs.stanford.edu/internal/stats2?rand=1">Statistics2</a>:an overview of the positive ratio of the 4001 WordNet synsets.(sorted by estimated positive number of models) Please click the synset id to see the annotated results in each synset.</p>
<p><a href="https://shapenet.cs.stanford.edu/internal/anno?taskid=47723">Annotation</a>:a sample annotation interface.</p>
<p><a href="https://shapenet.cs.stanford.edu/internal/query?word=chair">Query</a>:show the retrieved models from 3D warehouse based on different query word. Change the word in the url to see different query results.</p>
</div>
</div>
</body>
</html>
'''
    return HttpResponse(html)

def stats1(request):
    rand = int(request.GET['rand'])
    conn = dbtool2.ConnDB()
    if rand==1:
        res1 = dbtool2.Query(conn, 'select synsetid, num_total, num_good, num_finished, synsetword from bbox_synset_dump join bbox_request_record2 using(synsetid) order by num_good/num_finished desc')
    else:
	res1 = dbtool2.Query(conn, 'select synsetid, num_total, num_good, num_finished, synsetword from bbox_synset join bbox_request_record2 using(synsetid) order by num_good/num_finished desc')
    #res1 = dbtool2.Query(conn, 'select taskid, synsetword from bbox_task join bbox_request_record2 as r using(synsetid)')
    num_good = list()
    num_finished = list()
    num_total = list()
    #taskid = list()
    synsetword = list()
    synsetid = list()
    for r1 in res1:
	synsetid.append(r1[0])
	num_total.append(r1[1])
	num_good.append(r1[2])
	num_finished.append(r1[3])
	synsetword.append(r1[4])
    result = dict()
    result['synsetid']=synsetid
    conn.close()
    result['num_total']=num_total
    result['num_good']=num_good
    result['num_finished']=num_finished
    result['synsetword']=synsetword
    output = json.dumps(result)
    html='''<!doctype html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="../../media/www/internal/files/bootstrap.min.css" rel="stylesheet"/>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script src="../../media/www/internal/files/bootstrap.min.js"></script>
<script src="../../media/www/internal/files/js_stats1.js"></script>
<script>
var result='''+output+''';
</script>
<title>VisualizeResult</title>
</head>

<body>
</body>
</html>
'''
    return HttpResponse(html)
    #return HttpResponse("Hello, world. test=%s." % request.GET['test'])
    #return HttpResponse('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n<!-- The HTML 4.01 Transitional DOCTYPE declaration-->\n<!-- above set at the top of the file will set     -->\n <!-- the browser"s rendering engine into           -->\n <!-- "Quirks Mode". Replacing this declaration     -->\n <!-- with a "Standards Mode" doctype is supported, -->\n <!-- but may lead to some differences in layout.   -->\n <html>\n <head>\n <meta http-equiv="content-type" content="text/html; charset=UTF-8">\n</head>\n<body>\nsss\n<iframe src="javascript:''" id="__gwt_historyFrame" tabIndex='-1' style="position:absolute;width:0;height:0;border:0"></iframe>\n</body>')

def stats2(request):
    rand = int(request.GET['rand'])
    conn = dbtool2.ConnDB()
    if rand==1:
        res1 = dbtool2.Query(conn, 'select synsetid, num_total, num_good, num_finished, synsetword from bbox_synset_dump join bbox_request_record2 using(synsetid) order by num_good/num_finished*num_total desc')
    else:
	res1 = dbtool2.Query(conn, 'select synsetid, num_total, num_good, num_finished, synsetword from bbox_synset join bbox_request_record2 using(synsetid) order by num_good/num_finished*num_total desc')
    #res1 = dbtool2.Query(conn, 'select taskid, synsetword from bbox_task join bbox_request_record2 as r using(synsetid)')
    num_good = list()
    num_finished = list()
    num_total = list()
    #taskid = list()
    synsetword = list()
    synsetid = list()
    for r1 in res1:
	synsetid.append(r1[0])
	num_total.append(r1[1])
	num_good.append(r1[2])
	num_finished.append(r1[3])
	synsetword.append(r1[4])
    result = dict()
    result['synsetid']=synsetid
    conn.close()
    result['num_total']=num_total
    result['num_good']=num_good
    result['num_finished']=num_finished
    result['synsetword']=synsetword
    output = json.dumps(result)
    html='''<!doctype html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="../../media/www/internal/files/bootstrap.min.css" rel="stylesheet"/>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script src="../../media/www/internal/files/bootstrap.min.js"></script>
<script src="../../media/www/internal/files/js_stats2.js"></script>
<script>
var result='''+output+''';
</script>
<title>VisualizeResult</title>
</head>

<body>
</body>
</html>
'''
    return HttpResponse(html)

def query(request):
    word = request.GET['word']
    conn = dbtool.ConnDB()
    res = dbtool.Query(conn, 'select qid from query where word="%s"' % word)
    qid, = res[0]
    print qid
    res = dbtool.Query(conn, 'select modelid from annotation where qid=%d' % qid)
    i = 0
    modelset = list()
    for modelid, in res:
	modelset.append(modelid)
	print modelid
	i += 1
	if i > 100:
	    break

    html = '<body>'
    html += '<table>'
    for r in range(20):
	html += '<tr>'
	for c in range(5):
	    mid = modelset[r * 5 + c]
	    p = '../../media/warehouse/' +mid[0]+'/'+mid[1]+'/'+mid[2]+'/'+mid[3]+'/'+mid[4]+'/'+mid[5:len(mid)]+'/'+ mid + '/' + 'Image' + '/' + mid + '.bin'
	    html += '<td>'
	    html += '<img width="200px" src="%s">' % p
	    html += '</td>'
	html += '</tr>'
    html += '</table>'
    html += '</body>' 
    print html
    return HttpResponse(html)

def getimages(request):
    word = request.GET['word']
    start = int(request.GET['start'])
    end = int(request.GET['end'])

    result = dict()
    conn = dbtool.ConnDB()
    res = dbtool.Query(conn, 'select qid from query where word="%s"' % word)
    qid = res[0][0]
    res = dbtool.Query(conn, 'select count(*) from annotation where qid=%d' % qid)
    result['count'] = res[0][0]

    if end > 0 and end > start:
	res = dbtool.Query(conn, 'select modelid from annotation where qid=%d limit %d, %d' % (qid, start, end - start))
	images = list()
	for mid, in res:
	    # p = 'http://orions.stanford.edu:8000/media/' + mid + '/' + 'Image' + '/' + mid + '.bin'
	    p = 'https://shapenet.cs.stanford.edu/warehouse/' + mid + '/' + 'Image' + '/' + mid + '.bin'
	    images.append({'id':mid, 'url':p})
	result['images'] = images
    conn.close()

    output = json.dumps(result)
    return HttpResponse(output)

def cluster(request):
    word = request.GET['word']
    result = dict()
    rootDir = '../../media/www/internal/files/images/clustering/'+word+'/'
    count = 1
    for lists in os.listdir(rootDir):
	path = os.path.join(rootDir, lists)
	if os.path.isdir(path):
	    result[str(count)] = list()
	    for filelist in os.listdir(path):
	        result[str(count)].append(os.path.join(path, filelist)) 
	    count = count+1
    output = json.dumps(result)
    html = '''<!doctype html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="../../media/www/internal/files/bootstrap.min.css" rel="stylesheet"/>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script src="../../media/www/internal/files/bootstrap.min.js"></script>
<script src="../../media/www/internal/files/js_forclustering.js"></script>
<script>var result='''+output+''';</script>
<title>EvaResult</title>
</head>

<body style="dmargin: 0px;">

<div class="container" style="margin-top: 10px; width:1200px;">
<br>
  <div class="row-marketing">
	<div class="jumbotron ui-layout-container col-xs-12" style="overflow:hidden; postion:relative height:800px; padding-top:40px; padding-bottom:40px; padding-left:40px; padding-right:40px">
  	<ul class="nav nav-tabs" id="tabul">
  	</ul>
    
  	<div class="tab-content" id='tabdiv'>
	</div>
  </div>
 
  </div>
</div>
</body>
</html>
'''
    return HttpResponse(html)

@xframe_options_exempt
def verifyindex(request):
    try:
      rootpath = '/orions-zfs/projects/haosu/ShapeNet/Code/pycode/media/ImagesToVerify'
      verifyFoldersAll = glob.glob(os.path.join(rootpath,'*','*_verify','*'))
      verifyFoldersAll.sort()
      veriList = list()
      for veri in verifyFoldersAll:
	try:
	  imAll = open(os.path.join(veri,'img2verify.txt')).readlines()
	  batchTotal = int(math.ceil(float(len(imAll))/float(102)))
	  veri = veri.split('/')
	  for i in range(1,batchTotal+1):
	    veriList.append('taskname='+veri[-3]+'&iterNum='+veri[-2]+'&prefix='+veri[-1]+'&batchNum='+str(i))
	except:
	  continue
      result = dict()
      result['veriList'] = veriList
      output = json.dumps(result)
      html='''<!doctype html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="../../media/www/internal/files/bootstrap.min.css" rel="stylesheet"/>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script src="../../media/www/internal/files/bootstrap.min.js"></script>
<script src="../../media/www/internal/files/verifyindexjs.js"></script>
<script>
var result='''+output+''';
</script>
<title>VerificationIndex</title>
</head>

<body style="dmargin: 0px;">

<div class="container" style="margin-top: 10px; width:1200px;">
<br>
<div id="mainlist" class="jumbotron ui-layout-container col-xs-12" style="overflow:hidden; postion:relative height:800px; padding-top:20px; padding-bottom:40px; padding-left:40px; padding-right:20px">

</div>
</div>
</body>
</html>
''' 
      return HttpResponse(html)
    except:
      print sys.exc_info()
      return HttpResponse(sys.exc_info())

@xframe_options_exempt
def verifyi(request):
    try:
      taskname = request.GET['taskname'] #simCosegBagSNCJune3_handle
      iterNum = request.GET['iterNum'] #iter1_verify
      prefix = request.GET['prefix'] #2ca6df7a5377825cfee773c7de26c274
      batchNum = int(request.GET['batchNum']) #1
      rootpath = '/orions-zfs/projects/haosu/ShapeNet/Code/pycode/media/ImagesToVerify'
      curSet = taskname[8:]
      curPart = curSet.split('-')[1]
      curSet = curSet.split('SNC')[0]
      tmp = open(os.path.join(rootpath,taskname,iterNum,prefix,'img2verify.txt')).readlines()
      img_cur = []
      for img in tmp[(batchNum-1)*102:batchNum*102]:
	img = img.strip().split(' ')
        img_cur.append({'imageid':img[0], 'imagename':os.path.join('../../media/ImagesToVerify',taskname,iterNum,prefix,img[1])})
      result = dict()
      result['img_cur']=img_cur
      result['curSet'] = curSet
      result['curPart'] = curPart
      output = json.dumps(result)
      html='''<!doctype html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="../../media/www/internal/files/bootstrap.min.css" rel="stylesheet"/>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script src="../../media/www/internal/files/bootstrap.min.js"></script>
<script src="../../media/www/internal/files/verifyjs.js"></script>
<script>
var result='''+output+''';
</script>
<title>Verification</title>
</head>

<body style="dmargin: 0px;">

<div class="container" style="margin-top: 10px; width:1200px;">
<br>
<div class="row-marketing">
<div class="jumbotron ui-layout-container col-xs-8" style="overflow:hidden; postion:relative height:800px; padding-top:20px; padding-bottom:40px; padding-left:40px; padding-right:20px">
<div class="row-marketing">
  <ul class="nav nav-tabs col-xs-4">
    <li class="active"><a href="#home" data-toggle="tab">Home</a></li>
  </ul>
</div>
<br><br><br>
<div class="row-marketing well" style="overflow:hidden;">
<div>
    <p id="curGloss" style="font-size:16px; font-weight:bold; font-style:border; margin-bottom:2px"></p>
</div>
</div>

  <div class="tab-content">
      <div class="tab-pane active" id="home">
	  <div id="imagespanel">
	    <ul class="col-xs-12">  
	    </ul>
	  </div>
    </div>
</div>
</div>

<div class="col-xs-1" style="overflow:hidden; postion:relative;">
</div>
<div id="selectedpanel" class=" col-xs-3" style="overflow:scroll; postion:relative;height:1952px;background-color:#eee; padding-top:20px; padding-bottom:20px; border-top: 1px solid #e5e5e5; border-bottom: 1px solid #e5e5e5; border-radius:6px;">
<div class="col-xs-12">
</div>
</div>

</div>
</div>
<!--div style="text-align:center; margin-bottom:30px">
<input id="submit" type="button" value="Submit" style="border-radius:3px"></input>-->
<div style="text-align:center; margin-bottom:30px">
<form action="javascript:subresult()">
<input id="submit" type="submit" name="commit1" value="Submit" style="border-radius:3px"></input>
</form>
<form id="mturk_form" action="https://www.mturk.com/mturk/externalSubmit" method="POST"><input type="hidden" id="assignmentId" name="assignmentId" value=""><input type="submit" name="commit2" value="Submit" hidden><input type="hidden" id="num_good" name="num_good" value=""><input id="num_total" type="hidden" name="num_total" value=""></form>
</div>
</body>
</html>
''' 
      return HttpResponse(html)
    except:
      print sys.exc_info()
      return HttpResponse(sys.exc_info())


@csrf_exempt
@xframe_options_exempt
def verifys(request):
    if request.method == 'POST':
	selectedId = json.loads(request.POST.get('selectedId'))
	allId = json.loads(request.POST.get('allId'))
	assignmentId = request.POST.get('assignmentId')
	if assignmentId=="":
	  assignmentId="none"
	taskname = request.POST.get('taskname')
	iterNum = request.POST.get('iterNum')
	prefix = request.POST.get('prefix')
	batchNum = request.POST.get('batchNum')

	fileOut = open(os.path.join('/orions-zfs/projects/haosu/ShapeNet/Code/pycode/media/ImagesToVerify/',taskname,iterNum,prefix,'batch'+batchNum+'_'+assignmentId+'.txt'),'w')
	for id in allId:
	  if id in selectedId:
	    fileOut.writelines(id+' 1\n')
	  else:
	    fileOut.writelines(id+' 0\n')
	fileOut.close()

	return HttpResponse(json.dumps("Thank you!"))
    else:
        return HttpResponse("Thank you.")


@csrf_exempt
@xframe_options_exempt
def rank(request):
    if request.method == 'GET':
        # TODO: write down your logic here. Basically write down annotation results to disk files
        with open('/orions3-zfs/projects/haosu/Image2Scene/testweb.tmp', 'w') as f:
            f.write('test')
	return HttpResponse(json.dumps("Thank you! I am ranker GET supporting hot deployment!")) 
    else:
	return HttpResponse(json.dumps("Thank you! I am ranker POST supporting hot deployment!")) 

global appScope
appScope = {}

@csrf_exempt
@xframe_options_exempt 
def demo(request):
    arg = request.GET.get('arg')
    if "eng" in appScope.keys():
        eng = appScope["eng"]
    else:
        eng = matlab.engine.start_matlab()
        appScope["eng"] = eng 

    if "imgList" in appScope.keys():
        imgList = appScope["imgList"] 
    else:
        imgList = eng.load("/orions-zfs/share/demo/imgNames.mat")['imgNames']
        appScope["imgList"] = imgList 

    imgList = [{'imagename' : x, 'imageid' : i} for i, x in enumerate(imgList)]
    output = json.dumps(imgList)
    html='''
<!doctype html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="../../media/www/internal/files/bootstrap.min.css" rel="stylesheet"/>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script src="../../media/www/internal/files/bootstrap.min.js"></script>
<script>
var imgList='''+output+''';
</script>
<script src="../../media/www/internal/files/js_demo.js"></script>
<script src="../../media/www/internal/files/dropzone.js"></script>
<title>Demo View-invariant Retrieval</title>
</head>

<body style="dmargin: 0px;">

<div class="container" style="margin-top: 10px; width:1200px;">
<br>
<div class="row-marketing">
    <div class="jumbotron ui-layout-container col-xs-3" style="overflow:hidden; postion:relative height:800px">
        <h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Query:</h3>
        <div class="jumbotron ui-layout-container col-xs-12" style="overflow:scroll; postion:relative height:800px; height:840px; width:200px; padding-top:20px; padding-bottom:40px; padding-left:40px; padding-right:20px">
            <div id="imagespanel_query">
                <ul class="col-xs-12">  
                </ul>
            </div>
        </div>
    </div>

    <div class="jumbotron ui-layout-container col-xs-9" style="overflow:hidden; postion:relative height:800px">
        <h3>&nbsp;&nbsp;&nbsp;HoG retrieval results:</h3>
        <div class="jumbotron ui-layout-container col-xs-12" style="overflow:scroll; postion:relative height:800px; height:400px; padding-top:20px; padding-bottom:40px; padding-left:40px; padding-right:20px">
            <div id="imagespanel_hog">
                <ul class="col-xs-12">  
                </ul>
            </div>
        </div>
            

        <h3>&nbsp;&nbsp;&nbsp;Our view-agnostic retrieval results:</h3>
        <div class="jumbotron ui-layout-container col-xs-12" style="overflow:scroll; postion:relative height:800px; height:400px; padding-top:20px; padding-bottom:40px; padding-left:40px; padding-right:20px">
            <div id="imagespanel_vad">
                <ul class="col-xs-12">  
                </ul>
            </div>
        </div>
    </div>
</div>

</body>
</html>
''' 
    return HttpResponse(html)
    #return HttpResponse(output)


@csrf_exempt
@xframe_options_exempt 
def demoqueryOld(request):
    global appScope
    qid = int(request.GET.get('qid'))
    isStartMatlab = False
    if "eng" in appScope.keys():
        eng = appScope["eng"]
    else:
        eng = matlab.engine.start_matlab()
        isStartMatlab = True
        appScope["eng"] = eng 

    if "imgList" in appScope.keys():
        imgList = appScope["imgList"] 
    else:
        imgList = eng.load("/orions-zfs/share/demo/imgNames.mat")['imgNames']
        appScope["imgList"] = imgList 

    if "distMat_im" in appScope.keys():
        distMat_im = appScope["distMat_im"]
    else:
        distMat_im = eng.load("/orions-zfs/share/demo/distMat_im.mat")['distMat_im']
        appScope["distMat_im"] = distMat_im 

    if "distMat_VAD" in appScope.keys():
        distMat_VAD = appScope["distMat_VAD"]
    else:
        distMat_VAD = eng.load("/orions-zfs/share/demo/distMat_VAD.mat")['distMat_VAD']
        appScope["distMat_VAD"] = distMat_VAD 

    if "gt" in appScope.keys():
        gt = appScope["gt"]
    else:
        gt = eng.load("/orions-zfs/share/demo/gt.mat")['gt']
        gt = np.asarray([[y for y in x] for x in gt]) 
        appScope["gt"] = gt 

    row = distMat_im[qid]
    val, order = eng.sort(row, nargout=2)
    imOrder = [int(x)-1 for x in order[0]]

    row = distMat_VAD[qid]
    val, order = eng.sort(row, nargout=2)
    VADOrder = [int(x)-1 for x in order[0]]

    gt_query = gt[:, qid]
    totImg = len(imgList)
    hogGoodFlag = []
    for i in range(totImg):
        gt_res = gt[:, imOrder[i]]
        t1 = np.sum(np.abs(gt_query-gt_res))
        t2 = np.sum(gt_query) + np.sum(gt_res)
        if t1 < t2: # has intersection
            hogGoodFlag.append(1)
        else:
            hogGoodFlag.append(0) 

    VADGoodFlag = []
    for i in range(totImg):
        gt_res = gt[:, VADOrder[i]]
        t1 = np.sum(np.abs(gt_query-gt_res))
        t2 = np.sum(gt_query) + np.sum(gt_res)
        if t1 < t2: # has intersection
            VADGoodFlag.append(1)
        else:
            VADGoodFlag.append(0) 

    html = json.dumps({'hogOrder':imOrder, 'VADOrder':VADOrder, 'hogGoodFlag':hogGoodFlag, 'VADGoodFlag':VADGoodFlag, 'isStartMatlab':isStartMatlab})
    return HttpResponse(html)

def loadFromExternalApp(filepath):
    while not os.path.exists(filepath+'.done'):
	pass
    return json.load(open(filepath))

@csrf_exempt
@xframe_options_exempt 
def demoquery(request):
    qid = int(request.GET.get('qid'))

    N = 10
    
    baseFolder = '/tank0/projects/haosu/ShapeNet/Code/pycode/django_projects/firstapp/demoOfflineTMP'
    tag = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

    with open(os.path.join(baseFolder, tag+'.query'), 'w') as f: 
        f.write(str(qid))
    open(os.path.join(baseFolder, tag+'.query.done'), 'w').close()

    result = loadFromExternalApp(os.path.join(baseFolder, tag+'.result'))

    imgList = result['imgList']
    imOrder = result['imOrder']
    VADOrder = result['VADOrder']

    html = json.dumps({'hogOrder':imOrder, 'VADOrder':VADOrder})
    return HttpResponse(html)



@csrf_exempt
@xframe_options_exempt 
def demolive(request):
    html='''
<!doctype html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="../../media/www/internal/files/bootstrap.min.css" rel="stylesheet"/>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script src="../../media/www/internal/files/bootstrap.min.js"></script>
<script src="../../media/www/internal/files/js_demo.js"></script>
<script src="../../media/www/internal/files/dropzone.js"></script>
<link rel="stylesheet" href="../../media/www/internal/files/dropzone.css">
<title>Live Demo for View-invariant Retrieval</title>
</head>

<body style="dmargin: 0px;">
<div class="container" style="margin-top: 10px; width:1800px;">
<br> 
<div class="row-marketing">
    <form action="https://shapenet.cs.stanford.edu/internal/fileupload" method="POST" class="dropzone" enctype="multipart/form-data">
    </form>
    <form action="https://shapenet.cs.stanford.edu/internal/democrop">
    <input type="submit">
    </form>
</div>
</body>
</html>
''' 
    return HttpResponse(html)

def handle_uploaded_file(f):
    with open('/orions-zfs/projects/haosu/ShapeNet/Data/www/internal/demotmp/tmp.jpg', 'wb+') as dst:
        for chunk in f.chunks():
	    dst.write(chunk)

@csrf_exempt
# @xframe_options_exempt 
def fileupload(request):
    if request.method == 'POST':
	handle_uploaded_file(request.FILES['file'])
	# return HttpResponse(str(request.FILES))

        html = '''
    <div class="jumbotron ui-layout-container col-xs-12" style="overflow:hidden; postion:relative height:800px">

        <div class="jumbotron ui-layout-container col-xs-6" style="overflow:hidden; width:800px">
	    &nbsp;&nbsp;&nbsp;HoG retrieval results:
	    <div class="jumbotron ui-layout-container col-xs-12" style="overflow:scroll; postion:relative height:800px; height:400px; padding-top:20px; padding-bottom:40px; padding-left:40px; padding-right:20px">
		<div id="imagespanel_hog">
		    <ul class="col-xs-12">  
		    </ul>
		</div>
	    </div>
	</div>

        <div class="jumbotron ui-layout-container col-xs-6" style="overflow:hidden; width:800px">
	    &nbsp;&nbsp;&nbsp;Our view-agnostic retrieval results:
	    <div class="jumbotron ui-layout-container col-xs-12" style="overflow:scroll; postion:relative height:800px; height:400px; padding-top:20px; padding-bottom:40px; padding-left:40px; padding-right:20px">
		<div id="imagespanel_vad">
		    <ul class="col-xs-12">  
		    </ul>
		</div>
	    </div>
	</div>

    </div>
'''
	return HttpResponse('ok')

@csrf_exempt
# @xframe_options_exempt 
def democrop(request):
    html = '''
<!doctype html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="../../media/www/internal/files/global.css" rel="stylesheet" type="text/css" />
<link rel="stylesheet" href="../../media/www/internal/files/jquery.Jcrop.min.css" type="text/css" />
<link href="../../media/www/internal/files/jcrop_demos.css" rel="stylesheet" type="text/css" />

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<!--<script src="../../media/www/internal/files/jquery.min.js"></script>-->
<script src="../../media/www/internal/files/jquery.Jcrop.min.js"></script>
<script src="../../media/www/internal/files/jcrop_demos.js"></script>

<script>
$(function(){ $('#jcrop_target').Jcrop({
    onSelect : showCoords
}); });

function showCoords(c) {
    document.getElementById("x").value = c.x;
    document.getElementById("x2").value = c.x2;
    document.getElementById("y").value = c.y;
    document.getElementById("y2").value = c.y2;
}
</script>

<title>Live Demo for View-invariant Retrieval</title>
</head>

<body style="dmargin: 0px;">
<div class="container" style="margin-top: 10px; width:1800px;">
<br> 
<div class="row-marketing">
    <img src="https://shapenet.cs.stanford.edu/media/www/internal/demotmp/tmp.jpg" width="400px" id="jcrop_target" />
</div>
</div>

<div class="container" style="margin-top: 10px; width:1800px;">
<form action="https://shapenet.cs.stanford.edu/internal/demosearch" id="selection" methd="GET">
    <input type="hidden" id="x" name="x" value="0">
    <input type="hidden" id="y" name="y" value="0">
    <input type="hidden" id="x2" name="x2" value="10000">
    <input type="hidden" id="y2" name="y2" value="10000">
    <input type="submit">
</form>
</div>

</body>
</html>
    
'''
    return HttpResponse(html)

@csrf_exempt
@xframe_options_exempt 
def demosearch(request):
    if request.method == 'GET':
	x = request.GET['x']
	y = request.GET['y']
	x2 = request.GET['x2']
	y2 = request.GET['y2']

	N = 10
	baseFolder = '/tank0/projects/haosu/ShapeNet/Code/pycode/django_projects/firstapp/demoTMP'
	tag = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

	with open(os.path.join(baseFolder, tag+'.query'), 'w') as f: 
	    f.write(x + ' ' + y + ' ' + x2 + ' ' + y2)
	open(os.path.join(baseFolder, tag+'.query.done'), 'w').close()

	result = loadFromExternalApp(os.path.join(baseFolder, tag+'.result'))

	imgList = result['imgList'][0]
	hogOrder = result['imOrder']
	VADOrder = result['VADOrder']
	hogRanking = result['hogRanking']
	VADRanking = result['VADRanking']

	imgList = [{'imagename' : x, 'imageid' : i} for i, x in enumerate(imgList)]
	output = json.dumps(imgList)
	html='''
<!doctype html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link href="../../media/www/internal/files/bootstrap.min.css" rel="stylesheet"/>

<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
<script src="../../media/www/internal/files/bootstrap.min.js"></script>
<script>
var imgList='''+output+''';
var hogOrder = ''' + json.dumps(hogOrder) + ''';
var VADOrder = ''' + json.dumps(VADOrder) + '''; 
var hogRanking = ''' + json.dumps(hogRanking) + ''';
hogRanking = hogRanking[0];
var VADRanking = ''' + json.dumps(VADRanking) + ''';
VADRanking = VADRanking[0];

var numSelectedView = hogRanking.length;
</script>
<style type="text/css">
.scroll {
width:800px;
height:120px;
// margin:100px auto;
background:#FFFFFF;
border:2px solid #000;
overflow:auto;
white-space:nowrap;
box-shadow:0 0 10px #000;
}
.scroll img {
margin:20px 10px 0 10px;
}
</style>
<script src="../../media/www/internal/files/js_livedemo.js"></script>
<title>Demo View-invariant Retrieval</title>
</head>

<body style="dmargin: 0px;">
<div class="container" style="margin-top: 10px; width:1200px;">
<a href="https://shapenet.cs.stanford.edu/internal/demolive">try a new image</a> 
<br>
<div class="row-marketing">
    <div class="jumbotron ui-layout-container col-xs-3" style="overflow:hidden; postion:relative height:800px">
        <h3>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Query:</h3>
        <div class="jumbotron ui-layout-container col-xs-12" style="overflow:hidden; postion:relative height:800px; height:840px; padding-top:20px; padding-bottom:10px; padding-left:40px; padding-right:20px">
             <img src="https://shapenet.cs.stanford.edu/media/www/internal/demotmp/tmpCrop.jpg" width="100px"></img>
        </div>
    </div>

    <div class="jumbotron ui-layout-container col-xs-9" style="overflow:hidden; postion:relative height:800px">
        <h3>&nbsp;&nbsp;&nbsp;HoG retrieval results:</h3>
        <div id="imagespanel_hog1" class="scroll">
        </div>
        <div id="imagespanel_hog2" class="scroll">
        </div>
        <div id="imagespanel_hog3" class="scroll">
        </div>

        <h3>&nbsp;&nbsp;&nbsp;Our view-agnostic retrieval results:</h3>
        <div id="imagespanel_vad1" class="scroll">
        </div>
        <div id="imagespanel_vad2" class="scroll">
        </div>
        <div id="imagespanel_vad3" class="scroll">
        </div>
    </div>
</div>

</body>
</html>
''' 
    return HttpResponse(html)
