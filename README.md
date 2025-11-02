# WEEK6 MLOPS ASSIGNMENT SUBMISSION SEPT 2025 

## Submission by - Roll no - 21f1000243, Name - Santosh Kumar Verma, Mail - 21f1000243@ds.study.iitm.ac.in 

## MLOps : Continuous Deployment to Kubernetes

This project completes a full MLOps cycle by building a Continuous Deployment (CD) pipeline. The pipeline automatically builds a Docker image for the Iris model's FastAPI, pushes it to Google Artifact Registry, and deploys it to a Google Kubernetes Engine (GKE) cluster.

## 🛠️ Core Technologies

- GitHub Actions: For the automated CI/CD pipeline.

- FastAPI: To create the model's prediction API.

- Docker: For containerizing the application.

- Google Kubernetes Engine (GKE): For deploying and managing the container.

- Google Artifact Registry: To host the private Docker images.

## Workflow and Key Files

The pipeline is defined by a set of files that work together to build, package, and deploy the application.

| File | Purpose in the Workflow |
| :--- | :--- |
| **`iris_fastapi.py`** | The Python application code. It uses FastAPI to load the `model.joblib` and serve predictions at a `/predict/` endpoint. |
| **`v1/data.csv`, `v2/data.csv`** | Raw data files used to re-train a compatible model. |
| **`retrain.py`** | A utility script used to re-train the model. This was necessary to fix a `KeyError` by creating a `model.joblib` file that matched the `scikit-learn` version in the Docker container. |
| **`model.joblib`** | The serialized, re-trained scikit-learn model, bundled directly into the Docker image. |
| **`requirements.txt`** | Lists all Python dependencies (`fastapi`, `gunicorn`, `scikit-learn`, etc.). Pinning versions here was critical for the model to load correctly. |
| **`Dockerfile`** | The "recipe" to build the application container. It copies all code, installs `requirements.txt`, and defines the `CMD` (using `gunicorn`) to run the API server. |
| **`deployment.yaml`** | The Kubernetes "manifest." It defines the **Deployment** (which Docker image to use, how many replicas) and the **Service** (how to expose the app to the internet with a `LoadBalancer`). |
| **`.github/workflows/cd.yml`** | The heart of the CD pipeline. This GitHub Actions file automates the entire process: (1) Builds the Docker image, (2) Pushes it to Artifact Registry, (3) Connects to GKE, and (4) Applies the `deployment.yaml` to deploy the new version. |

## 🐛 Challenges Faced

| Challenge | Error Message | Solution |
| :--- | :--- | :--- |
| **Pods Crashing** | `CrashLoopBackOff` / `KeyError: 60` | The `scikit-learn` version used to save the model was different from the one in the `Dockerfile`. **Fix:** Created `retrain.py` to build a new `model.joblib` using the *exact* library versions from `requirements.txt`. |
| **Deployment Fails** | `spec.template.spec.containers[0].image: Required value` | The `IMAGE_URL` variable was empty in the deploy job. GitHub's security scanner was blocking it as a potential secret. **Fix:** Combined the `build-and-push` and `deploy` jobs into a single GitHub Actions job. |
| **`kubectl` Fails** | `gke-gcloud-auth-plugin... not found` | The local SSH terminal was missing the GKE authentication plugin for `kubectl`. **Fix:** Installed the plugin with `sudo apt-get install google-cloud-sdk-gke-gcloud-auth-plugin`. |
| **`curl` Fails** | `Connection refused` | This was a symptom of the `CrashLoopBackOff` error. The Load Balancer had an IP but no healthy pods to route traffic to. Fixing the pods fixed this. |

## 💡 Key Learnings

- Version Pinning is Critical: The CrashLoopBackOff error was a classic MLOps problem. The environment used to train a model and the environment used to serve it must be identical. Pinning versions in requirements.txt is essential.

- Infrastructure as Code (IaC): Using deployment.yaml to define the Kubernetes state makes deployments repeatable and version-controlled.

- CI/CD Pipeline Security: GitHub Actions masks outputs it thinks are secrets, which can break multi-job workflows. Combining steps into a single job is a robust workaround.

## END
