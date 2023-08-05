from setuptools import setup

setup(name='svg_func',
      version='1.0.2',
      description='functions in svg for logo',
      author='xmn',
      author_email='2579015983@qq.com',
      url='https://www.python.org/',
      license='MIT',
      keywords='ga nn',
      project_urls={
            'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
            'Funding': 'https://donate.pypi.org',
            'Source': 'https://github.com/pypa/sampleproject/',
            'Tracker': 'https://github.com/pypa/sampleproject/issues',
      },
      packages=['interpolation'],
      install_requires=['numpy>=1.14', 'torch>=1.4.0','IPython>=7.27.0','moviepy>=1.0.3','networkx>=2.6.3',
                        'shapely>=1.7.1','torchvision','matplotlib','svgwrite','cairosvg','six >= 1.12.0',
                        'tensorflow','tensorboardX','pillow','svglib','tqdm','jupyter',
                        'scikit-image','pandas','numba','sklearn','umap-learn','umap-learn[plot]',
                        'kivy'],
      python_requires='>=3'
     )
