import re


def is_valid_ruby(ruby_text):
    # Regular expression to match individual ruby-rt pairs
    ruby_tag_pattern = r'<ruby>.*?<rt>.*?</rt>.*?</ruby>'

    # Check if all ruby tags have a corresponding rt tag in the correct order
    matches = re.findall(ruby_tag_pattern, ruby_text)

    # Check if every <ruby> has a corresponding <rt> inside
    if matches:
        # Ensure there is no unmatched <ruby> or <rt> left
        ruby_open = ruby_text.count('<ruby>')
        ruby_close = ruby_text.count('</ruby>')
        rt_open = ruby_text.count('<rt>')
        rt_close = ruby_text.count('</rt>')

        # Both ruby and rt counts should match in terms of open/close tags
        if ruby_open == ruby_close and rt_open == rt_close and ruby_open == rt_open:
            return True
    return False