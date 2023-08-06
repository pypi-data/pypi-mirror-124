# PySVGExport

![Python Version Support](https://img.shields.io/badge/python-3.6+-blue)
![PyPI Version](https://img.shields.io/pypi/v/pysvgexport?label=PyPI&logo=pypi)
[![GitHub license](https://img.shields.io/github/license/vantrong291/pysvgexport)](https://github.com/vantrong291/pysvgexport/blob/main/LICENSE)

## _SVGExport for Python_

Idea from [svgexport] using for nodejs

### Install via pip

```shell
pip3 install pysvgexport
```

### Usage

##### 1. Command-line

```shell
# See instruction
svgexport -h

# Export command example
svgexport -f SVG_FILE_PATH -s SCALE -o OUT_PUT_PNG
```

##### 2. Inside a Python project

```python
from pysvgexport import SVGExport

svg_data = '''
    <svg xmlns="http://www.w3.org/2000/svg"
         xmlns:xlink="http://www.w3.org/1999/xhtml" width="235.6875px" 
         height="112.37257096319047px" 
         viewBox="0 0 235.6875 112.37257096319047">
        <defs>
            <path d="M 29.050328462552656,81.24213909012583 A 120.43422075282764 
                     120.43422075282764 0&#10;    
                     0  1 206.63717153744733,81.24213909012583 Z" 
                  id="svg-text" />
        </defs>
        <text>
            <textPath xmlns:xlink="http://www.w3.org/1999/xhtml" 
                      xlink:href="#svg-text" lengthAdjust="spacing" 
                      fill="#1ebb6a" method="stretch" 
                      textLength="199.6875" spacing="auto" 
                      xml:space="preserve" 
                      style="font-size: 30px; 
                             letter-spacing: 0px; 
                             font-family: &quot;Aclonica.ttf&quot;;"
            >LALALALA text</textPath>
        </text>
    </svg>
'''
capture_options = {"scale": 20}
output_options = {"omitBackground": True}
svg_exporter = SVGExport(svg_data=svg_data, 
                         capture_options=capture_options, 
                         output_options=output_options)
image = svg_exporter.execute()
```

[svgexport]: <https://github.com/shakiba/svgexport>