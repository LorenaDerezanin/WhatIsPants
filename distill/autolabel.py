from autodistill.detection import CaptionOntology
from autodistill_grounded_sam import GroundedSAM

# images imported from:
# https://github.com/yumingj/DeepFashion-MultiModal?tab=readme-ov-file


ontology = CaptionOntology({
    "pants": "pants",
    "jeans": "pants",
    "shorts": "pants",
    "trousers": "pants",
    "chinos": "pants"
})


# label dataset with base model using the classes given above (ontology)
base_model = GroundedSAM(ontology=ontology)
dataset = base_model.label(
    input_folder="images_subset",
    extension=".jpg",
    output_folder="dataset"
)



