class HTML:
    def __init__(self,output=None, tags=['<html>']):
        self.output = output
        self.tags = tags

    def __add__(self, tag):
        self.tags.append(tag)
        return self


    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.tags.append('</html>')
        if self.output is None:
            for el in self.tags:
                print(el)
        else:
            with open(self.output, 'w') as f:
                for el in self.tags:
                    print(el, file=f)

class TopLevelTag:
    def __init__(self, tag, **attributes):
        self.tag = tag
        self.attributes = attributes
        self.children = []

    def __enter__(self):
        return self
    def __exit__(self, type, value, backtrace):
        return self

    def __str__(self):
        attrs = []
        for k,v in self.attributes.items():
            if ',' in v:
                v = v.replace(',','')
            attrs.append('%s="%s"' %(k,v))
        attrs = " ".join(attrs)

        opening = "<%s>\n" %self.tag
        if attrs:
            opening = "<{tag} {attrs}>\n".format(tag=self.tag, attrs=attrs)
        internal = ""
        if self.children:
            for child in self.children:
                internal += "\t"+str(child)+'\n'
        ending = "</%s>" %self.tag
        return opening + internal + ending

    def __add__(self, child):
        self.children.append(child)
        return self


class Tag:
    def __init__(self,tag,is_single=False, **attributes):
        self.tag = tag
        self.is_single = is_single
        self.attributes = attributes
        self.children = []
        self.text = ""

    def __enter__(self):
        return self

    def __exit__(self, type, value, backtrace):
        return self

    def __add__(self, child):
        self.children.append(child)
        return self

    def __str__(self):
        attrs = []
        for k,v in self.attributes.items():
            if ',' in v:
                v = v.replace(',','')
            if '_' in k:
                k = k.replace('_', '-')
            if k == "klass":
                k = "class"
            if type(v) == tuple:
                v = ' '.join(v)
            attrs.append('%s="%s"' %(k,v))
        attrs = " ".join(attrs)

        if self.children:
            opening = "<{tag} {attrs}>\n".format(tag=self.tag, attrs=attrs)
            internal = "%s" %self.text
            for child in self.children:
                internal += "\t\t"+str(child)
            ending = "\t</%s>" %self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag} {attrs}/>\n".format(tag=self.tag, attrs=attrs)
            else:
                return "<{tag} {attrs}>{text}</{tag}>\n".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )


with HTML(output="test.html") as doc:
    with TopLevelTag("head") as head:
        with Tag("title") as title:
            title.text = "hello"
            head += title
    doc += head
    with TopLevelTag("body") as body:
        with Tag("h1", klass=("main-text")) as h1:
            h1.text = "Test"
            body += h1
        with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
            with Tag("p") as paragraph:
                paragraph.text = "another test"
                div += paragraph

            with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
               div += img

            body += div
    doc += body
