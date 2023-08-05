
![https://yoonik.me/wp-content/uploads/2019/08/cropped-LogoV4_TRANSPARENT.png](https://yoonik.me/wp-content/uploads/2019/08/cropped-LogoV4_TRANSPARENT.png)

# YooniK BiometricInThings API: Python SDK & Sample

[![PyPi Version](https://img.shields.io/pypi/v/yk_bit.svg)](https://pypi.org/project/yk-bit/)
[![License](https://img.shields.io/github/license/dev-yoonik/YK-BiT-SDK-Python)](https://github.com/dev-yoonik/YK-BiT-Python/blob/master/LICENSE)


This repository contains the Python Module of the YooniK BiometricInThings API, an offering within [YooniK Services](https://yoonik.me)

For more information please [contact us](mailto:info@yoonik.me).

## Getting started

Installing from the source code:

```bash
python setup.py install
```

Use it:

Make sure you have added the environment key-values (YK_BIT_BASE_URL and YK_BIT_X_API_KEY). Machine restart could be required.

```python
from os import getenv
import yk_bit as YKB


# BiometricInThings API Environment Variables
EV_BASE_URL = getenv('YK_BIT_BASE_URL')
EV_API_KEY = getenv('YK_BIT_X_API_KEY')

YKB.BaseUrl.set(EV_BASE_URL)
YKB.Key.set(EV_API_KEY)

# Verifies the camera availability status
if YKB.bit.status() == YKB.BiTStatus.Available:
    
    captured = YKB.capture(capture_timeout=10, anti_spoofing=True, live_quality_analysis=True)
    print(captured)
    
    verified = YKB.verify(reference_image=captured.image, capture_time_out=10, matching_score_threshold=0.8)
    print(verified)
    
    verified_images = YKB.verify_images(probe_image=verified.verified_image, reference_image=captured.image, matching_score_threshold=0.8)
    print(verified_images)


```


## Running the sample

A sample python script is also provided in 'sample' folder.

Run:

```bash
python run_bit_sample.py
```
