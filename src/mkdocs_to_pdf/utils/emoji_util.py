import re
from base64 import b64encode
from logging import Logger
from bs4 import PageElement


def fix_twemoji(soup: PageElement, logger: Logger = None):
    """ (workaround) replace <svg> to <img + b64encoded data/>

    cause, don't shown WeasyPrint 51
    for after material v4.5.0

    @see https://github.com/squidfunk/mkdocs-material/pull/1330
    """

    def fix_size(svg):
        '''
        svg['width'] = 24
        svg['height'] = 24
        '''
        view_box = _parse_view_box(svg['viewbox'])  # cspell:disable-line
        width, height = (
            view_box[2] - view_box[0],
            view_box[3] - view_box[1]
        )
        svg['width'] = int(width)
        svg['height'] = int(height)
        svg['style'] = 'fill: currentColor;'

    if logger:
        logger.debug('Converting emoji SVG to img(workaround).')

    for svg in soup.select('.twemoji svg'):
        try:
            fix_size(svg)
            encoded = b64encode(str(svg).encode('utf-8')).decode('ascii')
            data = "data:image/svg+xml;charset=utf-8;base64," + encoded
            img = soup.new_tag('img', src=data,
                               **{'class': 'converted-twemoji'})
            svg.replace_with(img)

            if logger:
                logger.debug(f'> svg: {svg}')
                logger.debug(f'< img: {img}')

        except Exception as e:
            if logger:
                logger.warning(f'Failed to convert SVG: {e}')
            pass


def _parse_view_box(view_box_string):
    """ parse svg viewBox """
    p = re.compile(r'(-?[\d\.]+) (-?[\d\.]+) (-?[\d\.]+) (-?[\d\.]+)')
    m = p.match(view_box_string)
    return (
        float(m.group(1)), float(m.group(2)),
        float(m.group(3)), float(m.group(4))
    )
