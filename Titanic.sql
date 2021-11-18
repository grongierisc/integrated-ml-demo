drop model titanic_survived

create model titanic_survived predicting ( Survived Boolean)  from Titanic_Table.Passenger

create model titanic_survived_h2o predicting ( Survived Boolean)  from Titanic_Table.Passenger USING { "ml_provider": "H2O" }

train model titanic_survived from Titanic_Table.Passenger

train model titanic_survived_h2o from Titanic_Table.Passenger USING { "ml_provider": "H2O","max_runtime_secs" : 500 }

SELECT TOP 20 PREDICT(titanic_survived), Survived from Titanic_Table.Passenger

VALIDATE MODEL titanic_survived from Titanic_Table.Passenger

SELECT 
TrainedModel, ID, ModelInfo, element_key
FROM %ML.TrainedModel_ModelInfo

SELECT 
ID, MetricName, MetricValue, TargetValue, ValidationRun
FROM %ML.ValidationMetric

insert into  Titanic_Table.Passenger
values (33,2,NULL,'A36',1,'St Louis, MO','S',30.0000,'Guillaume, Mr. Rongier',0,'male',0,NULL,777777)
insert into  Titanic_Table.Passenger
values (29,2,NULL,'B5',1,'St Louis, MO','S',211.3375,'Virginie, Miss. Rongier',0,'female',0,NULL,24160)
insert into  Titanic_Table.Passenger
values (70,2,NULL,'B5',3,'St Louis, MO','S',211.3375,'Virginie, Miss. Rongier',0,'female',0,NULL,24160)

SELECT PREDICT(titanic_survived), Survived from Titanic_Table.Passenger where Name like '%Rongier%'





create model test predicting ( diabetic String)
FROM QuickML_hdh.diabetic

train model test FROM QuickML_hdh.diabetic

select TOP 20  predict(test),* 
FROM QuickML_hdh.diabetic