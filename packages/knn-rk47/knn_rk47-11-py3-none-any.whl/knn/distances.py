import hnswlib
import numpy as np
from google.cloud import bigquery
from google.cloud.bigquery.table import RowIterator

from importlib_resources import files
from importlib_resources import as_file

project = "podcast-recs"
client = bigquery.Client()


def readTable(dataset, table) -> RowIterator:
    d_ref = bigquery.DatasetReference(project, dataset)
    t_ref = d_ref.table(table)
    return client.list_rows(t_ref)


def read_data(dataset, table):
    rit = readTable(dataset, table)
    vectors = [r.get("vector") for r in rit]
    return vectors


def make_index(vectors):
    dim = len(vectors[0])
    elements = len(vectors)
    ids = np.arange(elements)

    p = hnswlib.Index(space="cosine", dim=dim)
    p.init_index(max_elements=elements, ef_construction=200, M=16)
    p.add_items(vectors, ids)
    p.set_ef(50)

    return p


def index_from_table(dataset, table):
    vectors = read_data(dataset, table)
    return make_index(vectors)


def get_distances(p, vectors, k=1):
    labels, distances = p.knn_query(vectors, k=k)
    return labels, distances


"""save to file fn"""


def save(fn, p):
    p.save_index(fn)


"""loads from resource file in resources directory"""


def load(fn="index.bl", dim=64):
    p = hnswlib.Index(space="cosine", dim=dim)
    source = files("knn").joinpath(fn)
    with as_file(source) as sfn:
        fn = f"{sfn.parent}/{sfn.name}"
        print(fn)
        p.load_index(fn)
    return p


def test():
    src = files("knn").joinpath("a.txt")
    with as_file(src) as sfn:
        fn = f"{sfn.parent}/{sfn.name}"
        data = ftxt(fn)
        print(data)
        return data


def ftxt(fn):
    with open(fn, "r") as f:
        return f.read()


if __name__ == "__main__":

    dataset = "test_datasets"
    table = "tiny_vectors"
    test()
    # table = "english_show_shows_20211009"
    # vectors = read_data(dataset, table)
    # p = load()
    # ls, ds = get_distances(p.vectors)
    # print(ls, ds)
