from kfp import components

from google.cloud import storage


class KubeFlowHandler(object):

    def __init__(self):
        self.storage_client = storage.Client()

    def load_kfp_component(self, filename: str, bucket_id: str = 'tadd-kubeflow-components') -> components:

        bucket = self.storage_client.get_bucket(bucket_id)

        blob = bucket.blob(filename)
        blob = blob.download_as_string()
        blob = blob.decode('utf-8')

        blob_string = str(blob)

        return components.load_component_from_text("""{}""".format(blob_string))


if __name__ == '__main__':
    from kfp.v2 import compiler
    from kfp.v2 import dsl

    kf = KubeFlowHandler()

    run_query_with_destination = kf.load_kfp_component(
        "run-bigquery-query-with-destination/component.yaml")

    print("test")


    @dsl.pipeline(
        name='okpid-batch-reload-pipe',
        description='This is the batch reload pipeline for the webshop history dashboard',
    )
    def test_pipe():
        src_data_query_job_id = run_query_with_destination(query="SELECT * FROM `spielwiese-tobias.test.dest` LIMIT 10",
                                                           dest_project_id='spielwiese-tobias',
                                                           dest_dataset_id='test',
                                                           dest_table_id='temp_test_table')


    if __name__ == '__main__':
        compiler.Compiler().compile(pipeline_func=test_pipe,
                                    package_path='./pipe-spec.json')  # Local run: './cloud_function/pipe-spec.json'












