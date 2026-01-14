from html.parser import HTMLParser

class TagBalancer(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        # Tags that don't need closing or are self-closing in HTML5 (void elements)
        self.void_elements = {
            'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 
            'link', 'meta', 'param', 'source', 'track', 'wbr'
        }

    def handle_starttag(self, tag, attrs):
        if tag not in self.void_elements:
            self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in self.void_elements:
            return
            
        if not self.stack:
            self.errors.append(f"Unexpected end tag </{tag}> at {self.getpos()}")
            return

        last_tag, last_pos = self.stack[-1]
        if last_tag == tag:
            self.stack.pop()
        else:
            # Mismatch
            # Try to find the tag in the stack (maybe intermediate tags were unclosed)
            found = False
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    # Found it. Everything after it was unclosed.
                    unclosed = self.stack[i+1:]
                    for t, p in unclosed:
                        self.errors.append(f"Unclosed tag <{t}> at {p}")
                    # Pop everything up to and including this tag
                    self.stack = self.stack[:i]
                    found = True
                    break
            
            if not found:
                self.errors.append(f"Unexpected end tag </{tag}> at {self.getpos()} - Expected </{last_tag}>")

    def check_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        self.feed(content)
        
        if self.stack:
            for tag, pos in self.stack:
                self.errors.append(f"Unclosed tag <{tag}> at {pos} at end of file")
        
        if not self.errors:
            print("No tag balance errors found.")
        else:
            print("Found errors:")
            for e in self.errors:
                print(e)

checker = TagBalancer()
checker.check_file('preview_v2.html')
