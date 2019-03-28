#!/bin/bash

/Library/Tomcat/bin/shutdown.sh
/Library/Tomcat/bin/startup.sh
mvn compile tomcat7:deploy
echo "****************"
echo "TOMCAT RESTARTED"
echo "GO TO localhost:8080/WeatherServer"
