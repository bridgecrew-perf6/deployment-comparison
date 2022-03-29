import ray
from ray import serve
from transformers import pipeline

ray.init(address="auto", namespace="serve")
serve.start(detached=True)


# route_prefix defines name of HTTP query
@serve.deployment(name="http_deployment",
                  route_prefix="/summarize",
                  _autoscaling_config={
                      "min_replicas": 1,
                      "max_replicas": 5,
                      "target_num_ongoing_requests_per_replica": 10,
                  },
                  version="v1")
class Summarizer:
    def __init__(self):
        self.summarize = pipeline("summarization", model="t5-small")

    def __call__(self, request) -> str:
        txt = request.query_params["txt"]
        return self.get_summary(txt)

    def get_summary(self, txt: str) -> str:
        summary_list = self.summarize(txt)
        summary = summary_list[0]["summary_text"]
        return summary

    def hello_world(self, name: str) -> str:
        return f"hello world my name is {name}"


Summarizer.options(
    version="v1",
    name="1",
    ray_actor_options={
       "num_cpus": 1,
    },
).deploy()


# handle = Summarizer.get_handle()
# print(ray.get(handle.hello_world.remote("Max")))
