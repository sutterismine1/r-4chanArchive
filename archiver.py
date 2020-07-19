def main(postID):
    #!/usr/bin/env python
    # -*- coding: utf-8 -*-
    import praw
    import snudown
    import datetime
    import time
    import re
    import sys, os
    from requests.exceptions import HTTPError

    """ 
    Customization Configuration

    """
    # Path to which to output the file #
    outputFilePath='.\\'
    # The Path to the stylesheet, relative to where the html file will be stored #
    pathToCSS = outputFilePath + 'css/style.css'

    """
    Reddit Post Archiver
    By Samuel Johnson Stoever
    """
    print(os.path.abspath('.'))
    offline_reading_path = outputFilePath + "\\offline_reading\\"
    outputFilePath = offline_reading_path + postID + '.html'
    monthsList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


    def writeHeader(posttitle):
        htmlFile.write('<!DOCTYPE html>\n<html>\n<head>\n')
        htmlFile.write('\t<meta charset="utf-8"/>\n')
        htmlFile.write('\t<link type="text/css" rel="stylesheet" href="' + pathToCSS +'"/>\n')
        htmlFile.write('\t<title>' + posttitle + '</title>\n')
        htmlFile.write('</head>\n<body>\n')

    def parsePost(postObject):
        writeHeader(postObject.title)
        postObject.comments.replace_more(limit=0)
        postAuthorName = ''
        postAuthorExists = 0
        try:
            postAuthorName = postObject.author.name
            postAuthorExists = 1
        except AttributeError:
            postAuthorExists = 0
        htmlFile.write('<div class="title">\n')
        if postObject.is_self:
            # The post is a self post
            htmlFile.write(postObject.title)
            htmlFile.write('\n<br/><strong>')
        else:
            # The post is a link post
            htmlFile.write('<a id="postlink" href="' + postObject.url)
            htmlFile.write('">')
            htmlFile.write(postObject.title)
            htmlFile.write('</a>\n<br/><strong>')
        if postAuthorExists:
            htmlFile.write('Posted by <a id="userlink" href="' + "https://www.reddit.com/user/" + str(postObject.author))
            htmlFile.write('">')
            htmlFile.write(postAuthorName)
            htmlFile.write('</a>. </strong><em>')
        else:
            htmlFile.write('Posted by [Deleted]. </strong><em>')
        htmlFile.write('Posted at ')
        postDate = time.gmtime(postObject.created_utc)
        htmlFile.write(str(postDate.tm_hour) + ':')
        htmlFile.write(str(postDate.tm_min) + ' UTC on ')
        htmlFile.write(monthsList[postDate.tm_mon-1] + ' ')
        htmlFile.write(str(postDate.tm_mday) + ', ' + str(postDate.tm_year))
        htmlFile.write('. ' + str(postObject.ups - postObject.downs))
        if postObject.is_self:
            htmlFile.write(' Points. </em><em>(self.<a id="selfLink" href="')
        else:
            htmlFile.write(' Points. </em><em>(<a id="selfLink" href="')
        htmlFile.write("https://www.reddit.com/" + str(postObject.subreddit.url))
        htmlFile.write('">' + postObject.subreddit.display_name)
        if postObject.is_self:
            htmlFile.write('</a>)</em><em>')
        else:
            htmlFile.write('</a> Subreddit)</em><em>')
        htmlFile.write(' (<a id="postpermalink" href="https://www.reddit.com/')
        htmlFile.write(postObject.permalink)
        htmlFile.write('">Permalink</a>)</em>\n')
        if postObject.is_self:
            htmlFile.write('<div class="post">\n')
            htmlFile.write(postObject.selftext)
            htmlFile.write('</div>\n')
        else:
            htmlFile.write('<div class="post">\n<p>\n')
            if ".jpg" in postObject.url or ".png" in postObject.url:
                htmlFile.write('<img src="' + postObject.url)
                htmlFile.write("\">")
            else:
                htmlFile.write(postObject.url)
            htmlFile.write('</p>\n</div>\n')
        htmlFile.write('</div>\n')
        for comment in postObject._comments:
            parseComment(comment, postAuthorName, postAuthorExists)
        htmlFile.write('<hr id="footerhr">\n')
        htmlFile.write('<div id="footer"><em>Archived on ')
        htmlFile.write(str(datetime.datetime.utcnow()))
        htmlFile.write(' UTC</em></div>')
        htmlFile.write('\n\n</body>\n</html>\n')
        #Done
    def parseComment(redditComment, postAuthorName, postAuthorExists, isRoot=True):
        commentAuthorName = ''
        commentAuthorExists = 0
        try:
            commentAuthorName = redditComment.author.name
            commentAuthorExists = 1
        except AttributeError:
            commentAuthorExists = 0
        if isRoot:
            htmlFile.write('<div id="' + str(redditComment.id))
            htmlFile.write('" class="comment">\n')
        else:
            htmlFile.write('<div id="' + str(redditComment.id)) 
            htmlFile.write('" class="comment" style="margin-bottom:10px;margin-left:0px;">\n')
        htmlFile.write('<div class="commentinfo">\n')
        if commentAuthorExists:
            if postAuthorExists and postAuthorName == commentAuthorName:
                htmlFile.write('<a href="' + "https://www.reddit.com/user/" + str(redditComment.author))
                htmlFile.write('" class="postOP-comment">' + commentAuthorName + '</a> <em>')
            else:
                htmlFile.write('<a href="' + "https://www.reddit.com/user/" + str(redditComment.author))
                htmlFile.write('">' + commentAuthorName + '</a> <em>')
        else:
            htmlFile.write('<strong>[Deleted]</strong> <em>')
        htmlFile.write(str(redditComment.ups - redditComment.downs))
        htmlFile.write(' Points </em><em>')
        htmlFile.write('Posted at ')
        postDate = time.gmtime(redditComment.created_utc)
        htmlFile.write(str(postDate.tm_hour) + ':')
        htmlFile.write(str(postDate.tm_min) + ' UTC on ')
        htmlFile.write(monthsList[postDate.tm_mon-1] + ' ')
        htmlFile.write(str(postDate.tm_mday) + ', ' + str(postDate.tm_year))
        htmlFile.write('</em></div>\n')
        try:
            htmlFile.write(redditComment.body)
        except: print(redditComment.body)
        for reply in redditComment._replies:
            parseComment(reply, postAuthorName, postAuthorExists, False)
        htmlFile.write('</div>\n')
        #Done
    # End Function Definitions
    try:
        thePost = r.submission(id=postID)
        htmlFile = open(outputFilePath,'w+', encoding="utf-8")
        parsePost(thePost)
        htmlFile.close()
    except HTTPError: 
        print('Unable to Archive Post: Invalid PostID or Log In Required (see line 157 of script)')
    ##Done