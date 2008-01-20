# -*- coding: utf-8 -*-
import urllib, Image, os

def get_image_offset_sooa (size_orig, size_new, direction="center") :
	(w, h, ) = size_orig
	(w_new, h_new, ) = size_new

	# get image size ratio
	__pos = (0, 0, w_new, h_new, )

	if w > h : # resize height.
		__ratio = float(h_new) / float(h)
		h = h_new
		w = w * __ratio

		if direction == "topleft" :
			__offset_x0 = 0
			__offset_x1 = w_new
		else :
			if w > w_new :
				__offset_x0 = int(float(w - w_new) / float(2))
				__offset_x1 = int(w - float(w - w_new) / float(2))
			else :
				__offset_x0 = 0
				__offset_x1 = int(w)

		__pos = (
			__offset_x0,
			0,
			__offset_x1,
			int(h),
		)
	elif h > w : # resize width
		__ratio = float(w_new) / float(w)
		w = w_new
		h = h * __ratio

		if direction == "topleft" :
			__offset_y0 = 0
			__offset_y1 = h_new
		else :
			if h > h_new :
				__offset_y0 = int(float(h - h_new) / float(2))
				__offset_y1 = int(h - float(h - h_new) / float(2))
			else :
				__offset_y0 = 0
				__offset_y1 = h

		__pos = (
			0,
			__offset_y0,
			int(w),
			__offset_y1,
		)
	else : # height == width
		__offset_x0 = (w / 2) - (w_new - 2)
		__offset_x1 = __offset_x0 + w_new

		__offset_y0 = (h / 2) - (h_new - 2)
		__offset_y1 = __offset_y0 + h_new

		__pos = (
			__offset_x0,
			__offset_y0,
			__offset_x1,
			__offset_y1,
		)

	return ((int(w), int(h), ), __pos, )

def resize_image (path, size=(200, 200), mode="ratio", direction="center") :
	im = Image.open(path)

	(w, h, ) = im.size

	w_new = size[0]
	h_new = size[1]

	if w_new > w and h_new > h :
		return open(path, "rb").read()

	#if (w_new is not None or h_new is not None) and mode == "sooa" :

	if (w_new is not None or h_new is not None) and mode == "sooa" :
		((w, h, ), __pos, ) = get_image_offset_sooa(im.size, size, direction, )
		im = im.resize((w, h, ), Image.ANTIALIAS)
		im = im.crop(__pos)
	elif (w_new is not None or h_new is not None) and mode == "flickr_center" :
		if h_new and h > h_new :
			__ratio = float(h_new) / float(h)
			h = h_new
			w = w * __ratio

		# resizing
		im = im.resize((int(w), int(h), ), Image.ANTIALIAS)

		# center-focused crop
		if w > w_new :
			im = im.crop(
				(
					int(float(w - w_new) / float(2)),
					0,
					int(w - (float(w - w_new) / float(2))),
					h,
				)
			)
	elif (w_new is not None or h_new is not None) and mode == "flickr" :
		im = im.crop(
			(
				0,
				0,
				(w_new < w) and w_new or w,
				(h_new < h) and h_new or h,
			)
		)
	else :
		if w_new and w > w_new :
			__ratio = float(w_new) / float(w)
			w = w_new
			h = h * __ratio

		if h_new and h > h_new :
			__ratio = float(h_new) / float(h)
			h = h_new
			w = w * __ratio

		# resizing
		im = im.resize((int(w), int(h), ), Image.ANTIALIAS)

	__path = os.path.join("/tmp", urllib.quote(path, ""))
	try :
		im.save(__path, **im.info)
	except KeyError, e :
		__path += ".jpg"

		im.save(__path, **im.info)

	contents = open(__path, "rb").read()
	os.remove(__path)

	return contents


