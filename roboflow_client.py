from roboflow import Roboflow
rf = Roboflow(api_key="G2ooZSqVmMFkzPO9Y1J0")
project = rf.workspace().project("ww4")
model = project.version(1).model

# infer on a local image
print(model.predict("./images/a.jpg", confidence=40, overlap=30).json())

# visualize your prediction
model.predict("./images/a.jpg", confidence=40, overlap=30).save("prediction.jpg")
