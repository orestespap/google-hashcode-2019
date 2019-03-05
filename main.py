from saveandgrab import *

def create_image_struct():
	#Dictionary: photo id: [photo type, number of tags N, N strings ]
	
	images=dict.fromkeys(range(0,int(lines[0])))
	for index,aline in enumerate(lines[1::]):
		templist=aline.split(' ')
		templist[-1]=templist[-1].replace('\n','')
		images[index]=templist
	
	return images


def create_horizontal_slideshow():
	#If the tag is greater than the average count of tags, we look for the tag/2 (floor) tag bucket --> secondary tag count
	#If it isn't, we look for the tag*2 tag bucket --> secondary tag count. 
	#If the secondary tag doesn't exist, loop moves on to next tag bucket
	
	slideids=[] #A list of photo ids. Neighbooring pair of ids constitutes a slide.
	for primary_tag_count in tagbuckets:
		flag=0
		if primary_tag_count>averagetags:
			flag=1 

		if flag and tagbuckets.get(primary_tag_count//2):
			secondary_tag_count=primary_tag_count//2

			for aphotoid in tagbuckets[primary_tag_count]:
				if not isinslideshow[aphotoid]:
					matchkey=find_match(aphotoid,secondary_tag_count,True)
					if matchkey:
						slideids+=[aphotoid,matchkey]
						print('Slide added!')
		else:
			if tagbuckets.get(primary_tag_count*2) and not flag: #Checking if flag is false because you can't know which of the two conditions were false in the above conditional statement
				secondary_tag_count=primary_tag_count*2
				
				for aphotoid in tagbuckets[primary_tag_count]:
					if not isinslideshow[aphotoid]:
						matchkey=find_match(aphotoid,secondary_tag_count,False)
						if matchkey:
							slideids+=[aphotoid,matchkey]
							print('Slide added!')
	
	save_(slideids,'slideids.pickle') #Just in case
	return slideids

def find_match(aphotoid,secondary_tag_count,overaverage):

	for aphotoid2 in tagbuckets[secondary_tag_count]:
		
		if not isinslideshow[aphotoid2]:

			tag_intersect=set(images[aphotoid][2::]).intersection(set(images[aphotoid2][2::]))
			if overaverage:
				if len(tag_intersect)>=secondary_tag_count: #If count of common tags is greater or even than than the secondary tag, create slide and break the loop.
					isinslideshow[aphotoid],isinslideshow[aphotoid2]=True,True
					return aphotoid2
			else:
				if len(tag_intersect)<=secondary_tag_count and len(tag_intersect)!=0:
					isinslideshow[aphotoid],isinslideshow[aphotoid2]=True,True
					return aphotoid2
	return False



def inslideshow_struct():
	#Returns dictionary with ids as keys and boolean values indicating if photo is already in slideshow or not
	#True: photo is in slide show, False: photo is not in slide show
	return dict.fromkeys(range(0,int(lines[0])),False)

def tagbuckets_struct():
	#Each key is a count of tags found in the file, containing ids of photos that carry the particular count of tags
	#Returns only counts of tags that exist in the file
	
	maxnooftags=max(tuple(int(images[aphoto][1]) for aphoto in images))
	tagbuckets={primary_tag_count:tuple(animageid for animageid in images if primary_tag_count==int(images[animageid][1])) for primary_tag_count in range(1,maxnooftags+1)}
	
	return {countoftags:tupleofphotoids for countoftags,tupleofphotoids in tagbuckets.items() if tupleofphotoids}

def export_file():
	#slideids=grab_('slideids.pickle')
	for i in range(0,len(slideids)): slideids[i]=str(slideids[i])
	
	write_to_text_file('outputfile.txt',str(len(slideids)))
	write_to_text_file_args('outputfile.txt',*tuple(slideids))

#File structure
#First line: number of images
#Rest of the lines: Photo type, number of tags (N), TAGi-TAGn (N strings)

lines=list_lines_txt('b_lovely_landscapes.txt') #Average count of tags: 18
images=create_image_struct()
isinslideshow, tagbuckets, averagetags=inslideshow_struct(), tagbuckets_struct(), float(sum(int(images[animage][1]) for animage in images)/int(lines[0]))
slideids=create_horizontal_slideshow()
export_file()