# VOC2012_dataset_processing
I persent some python program about VOC2012/2007 datasets using and processing mehod.<br>
The processing program include:<br>
- 1.Select special category from the original VOC2012/2007 dataset. 1_extract_categroies.py <br>
- 2.Create val.txt and train.txt for training model. 2_creat_txt.py <br>
- 3.If annotate the datasets by youself, you could test whether the label file (.xml) is correct to the orignial image.3_test_annotation.py <br>
- 4.If the file name of annotations and images are out of order,you could re-sort and name the dataset files. 4_resort_rename.py <br>
- 5.In order to enhance the robust of training model, expanding and enhancing the datasets is a good idea.There is a enhancing datasets program include mirroring,rotation,brightness. 5_enhance_dataset.py <br>
