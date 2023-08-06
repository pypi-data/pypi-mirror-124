import logging
import knn.distances as ds

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

# to run:
# python -m knn_main --setup_file <path to setup.py>

class KNNDoFn(beam.DoFn):
    def setup(self):
        self.dim = 64
        self.index = ds.load("index.bl", self.dim)

    """Parse each line of input text into words."""

    def process(self, element):
        labels, scores = ds.get_distances(self.index, element.get("vector"))
        return [abs(score) for score in scores]


def run(argv=None):
    """Main entry point; defines and runs the wordcount pipeline."""

    # The pipeline will be run on exiting the with block.
    beam_options = PipelineOptions(
        # runner="DataflowRunner",
        runner="DirectRunner",
        project="podcast-recs",
        region="europe-west1",
        job_name="rkumar-test",
        temp_location="gs://recs_test/tmp/",
    )
    with beam.Pipeline(options=beam_options) as p:

        # Read the BQ table into a PCollection.

        # Read the BQ table into a PCollection.
        table_spec = "podcast-recs:test_datasets.tiny_vectors"
        lines = p | "Read" >> beam.io.ReadFromBigQuery(table=table_spec)
        counts = (
            lines
            | "Count" >> beam.ParDo(KNNDoFn())
            | "Mean" >> beam.combiners.Mean.Globally()
            | beam.Map(print)
        )


# To run:
# python -m knn --requirements_file requirements.txt
# > cat requirements.txt
# > google-cloud-bigquery
# >hnswlib
if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()
