[![Unit Tests](https://github.com/allanchua101/ipynta/actions/workflows/run_unit_tests.yml/badge.svg)](https://github.com/allanchua101/ipynta/actions/workflows/run_unit_tests.yml)

<p align="center">
    <img  src="https://i.imgur.com/mKCFKIf.jpeg"> 
</p>

<p align="center">
  <strong>ipynta</strong> is a Python library designed for rapid development of image pre-processing pipelines.
</p>

### High level overview

<p align="center">
  <img src="https://i.imgur.com/tCDKqJD.png" />
</p>

<p align="center">
  The diagram above describes the purpose of each iPynta class family and how can they be used collectively in an image pre-processing pipeline.
</p>

### Sourcing Classes

Sourcing classes are used for retrieving image dataset metadata from different sources (local drive, zip files, etc.):

- [DirectorySniffer](https://github.com/allanchua101/ipynta/blob/main/docs/sourcing/DirectorySniffer.md)

### Loader Classes

Loader classes are used for instantiating / constructing / loading images from different sources.

- [OpenCVLoader](https://github.com/allanchua101/ipynta/blob/main/docs/loaders/OpenCVLoader.md)
- [PillowLoader](https://github.com/allanchua101/ipynta/blob/main/docs/loaders/PillowLoader.md)

### Predicate Classes

Predicate classes are used for filtering unwanted data from image datasets.

- [DimensionPred](https://github.com/allanchua101/ipynta/blob/main/docs/predicates/DimensionPred.md)
- [GrayscalePred](https://github.com/allanchua101/ipynta/blob/main/docs/predicates/GrayscalePred.md)

### Why was it named ipynta?

`I-pinta` means _"to paint"_ in tagalog! This library is proudly developed by a Singapore-based Filipino lad with nothing better to do during evenings.
