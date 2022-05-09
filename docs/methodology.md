# Methodology
## web server
### dependencies

*backend*
- WSGI server: [Waitress](https://github.com/Pylons/waitress)
- WSGI library: [Werkzeug](https://wsgi.readthedocs.io/en/latest/)
- Web Framework: [Flask](https://github.com/pallets/flask)
- Database: [sqlite3](https://docs.python.org/3/library/sqlite3.html)

*frontend*
- CSS: Bootstrap

*device interconnection*
- method: REST API (refer to reference #1)
- library: Flask-RESTful

### process

*setup*

1. clone the source code into the machine:
`$ git clone https://github.com/jamestansx/webserver.git && cd webserver`

1. create a virtual environment:
`$ virtualenv venv`

1. activate the virtual env:%
`$ ./venv/Scripts/activate`

1. install all the dependencies:
`$ pip install -r requirements.txt`

*running the server*

1. start the server:
`$ waitress-server webserver:app`

### Data management

Using SQL

3 Tables:
- Users
- Device Info
- Data

Database relation diagram:

[![database relation diagram](https://mermaid.ink/img/pako:eNqVUsFuwyAM_RXL5_YHuFVrtnWTsqrtdsoFBXdFaiACsqlK8--DQKZkaQ8Lh4Dt5_f8oMVSC0KGZNaSfxpeFapQAI0lY6EN2_Bt8kP2lO3g3Yc3AravQyL_WO0enlcxo3hFs8SWW_utjYACT9yeSECdIgWG4i4SCvqSJUl11HPWdZ_reeGOose5otyr8aQRDL22CSF33F1qujHlIYQnY86U3OH70__GKD76784BFCYJP6ngZf-WT0aJl3W9LpedHhvJPCj6w5JPETYqGUCDGezXsQAadgkW-ANAt6MWE8QYEBcusCJTcSn8I2s7f2xq34gyIZ02yI78bGmBvHF6f1ElMmcaGorSk0xV3Q-TpNZu)](https://mermaid-js.github.io/mermaid-live-editor/edit#pako:eNqVUsFuwyAM_RXL5_YHuFVrtnWTsqrtdsoFBXdFaiACsqlK8--DQKZkaQ8Lh4Dt5_f8oMVSC0KGZNaSfxpeFapQAI0lY6EN2_Bt8kP2lO3g3Yc3AravQyL_WO0enlcxo3hFs8SWW_utjYACT9yeSECdIgWG4i4SCvqSJUl11HPWdZ_reeGOose5otyr8aQRDL22CSF33F1qujHlIYQnY86U3OH70__GKD76784BFCYJP6ngZf-WT0aJl3W9LpedHhvJPCj6w5JPETYqGUCDGezXsQAadgkW-ANAt6MWE8QYEBcusCJTcSn8I2s7f2xq34gyIZ02yI78bGmBvHF6f1ElMmcaGorSk0xV3Q-TpNZu)

```mermaid
erDiagram

  users {
      INTEGER UserId PK
      NVARCHAR Username
      NVARCHAR Password "hashed password"
  }

  deviceinfo {
      INTEGER DeviceId PK 
      INTEGER UserId FK
      NVARCHAR Name "Device name"
  }

  datatypes {
      INTEGER TypesId PK
      INTEGER DeviceId FK
      NVARCHAR Name
  }

  data {
      INTEGER DataId PK
      INTEGER DeviceId FK
      NVARCHAR Data "Data in JSON"
  }

  users ||--}o deviceinfo : "UserId: UserId"
  deviceinfo ||--}o datatypes: "DeviceId: DeviceId"
  data ||--o{ deviceinfo: "DeviceId:DeviceId"
```

### Device Interconnection

refer to [the sequence diagram](https://github.com/jamestansx/webserver/blob/main/README.md)


