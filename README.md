# MHP-RCA

### MHP-RCA: Multivariate Hawkes Process-based Root Cause Analysis in Microservice Systems

MHP-RCA is a Hawkes process-based RCA framework that integrate multi-source data.

## Environment
|ENVIRONMENT               |DETAIL                                                                                                                                             |
|---------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| **Hardware environment**  | CPU: 8-core 2.40GHz CPU, RAM: 16GB, OS: Ubuntu                                                                                                     |
| **Container environment** | Kubernetes 11.3.1, Docker Client 7.31, Docker Server 7.31                                                                                          |
| **Data collection**       | Metric collection: Istio 1.4.5, Prometheus 6.3, NodeExporter 1.41 ,Audit log collection: Elastic Search 8.4.1, Kibana 8.4.1, AuditBeat 8.4.1 |
| **Benchmark system**      | Bookinfo 1.17.0, Online-Boutique 0.8.0, Sock-Shop 0.4.8                                                                                            |

## Getting Started

**Clone the Repo**

```
git clone --depth=1 https://github.com/WHU-AISE/MHP-RCA.git
```

**Install Dependencies**

```
pip install -r requirements.txt
```

**Run**

```
python localization.py
```

