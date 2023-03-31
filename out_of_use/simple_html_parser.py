from html.parser import HTMLParser



class MyHTMLParser(HTMLParser):
    def __init__(self,allowed_tags):
        self.tags = []
        self._stack = []
        self.filered_string = ""
        self._allowed_tags = allowed_tags
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if self.is_supported_tag(tag):
            frame = {"begin" : len(self.filered_string) , "tag" : tag}
            self._stack.append(frame)
        else:
            # Ignore the tag
            self.filered_string += "<" + tag + ">"

    def handle_endtag(self, tag):
        if self.is_supported_tag(tag):
            # Case if we encounter an end tag at the begin
            if len(self._stack) >= 1:
                top = self._stack[len(self._stack) - 1]
                if top["tag"] == tag:
                    top["end"] = len(self.filered_string) - 1
                    self.tags.append(top)
                    self._stack.pop()
        else:
            # Ignore the tag
            self.filered_string += "</" + tag + ">"

    def handle_data(self, data):
        # Ignore data
        self.filered_string += data

    def is_supported_tag(self,tag: str) -> bool:
        return tag in self._allowed_tags

#with open("cooking_method.txt", 'r') as myfile:
#    data = myfile.read()
#
#allowed_tags = ["b","i","u","h1","h2","h3","h4","app:a"]
#parser = MyHTMLParser(allowed_tags)
#parser.feed(data)
