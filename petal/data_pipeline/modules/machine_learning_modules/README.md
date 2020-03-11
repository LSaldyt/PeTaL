# Machine Learning Modules 

PeTaL defines machine learning modules, which may fit into the entire framework via type dependencies, much like mining modules.
For instance, an image classifier will define an input type of "Image," which could come from, for instance, the `EOLImageModule`, 
which pulls images from EOL pages for particular organisms.

## Taxon Classifier Overview

For instance, PeTaL contains a `TaxonClassifier`, which does taxonomic classification based on images of organisms.
Currently, this consists of a convolutional neural network built on top of "EfficientNet". 
This model is defined using `pytorch` and resides in `data_pipeline/libraries/hierarchical_model`, where each model will also reside.
The *Module* (not to be confused with *Model*) resides in `data_pipeline/modules/machine_learning_modules/`, and is callable from the top level of `data_pipeline` by editing `settings.json`.
For instance, to set up an image classification workflow:

```json
{"scheduler:max_running" : 10,
 "scheduler:dependencies" : {"CatalogueOfLife" : {"in" : "None", "out" : "Taxon"},
                             "EOLImageModule" : {"in" : "Taxon", "out" : "Image"},
                             "TaxonClassifier" : {"in" : "Image", "out" : "None"},
                             },
 "pipeline:sleep_time" : 0.1,
 "pipeline:reload_time" : 30,
 "pipeline:blacklist" : [],
 "pipeline:whitelist" : ["CatalogueOfLife", "EOLImageModule", "TaxonClassifier"]}
```
Once the `settings.json` file is configured like this, the mining server can be started by calling the `./run` script in `data_pipeline`, or by manually running `python pipeline.py`.
When the server is started, it will first call `CatalogueOfLife`, which will generate `Taxon` objects within neo4j.
As these `Taxon` objects fill the database (and local server cache), instances of `EOLImageModule` will be spun up to download images on each `Taxon` and add them to the database.
In turn, as `Image`s come into the database, the server will train the `TaxonClassifier` on these images.
Any other type-dependent pipeline will have a process similar to this one.

## TaxonClassifier Detail

For additional detail on the implementation of a framework machine learning module, see the `TaxonClassifier` file. For detail on mining modules, see the `README.md` in `data_pipeline`, and specifically the mining modules `CatalogueOfLife.py` and `WikipediaModule.py`, which are intentionally well documented.
