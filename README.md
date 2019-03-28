# Power TAC Weather Server

The Power TAC Weather Server is a dynamic jsf web application for serving weather data from a database.

### Getting Started 

#### Create a database on a properly configured MySQL server.
* download and setup [mysql](https://dev.mysql.com/downloads/mysql/)
* and/or download and setup [workbench](https://dev.mysql.com/downloads/workbench/)
* once setup: create the database and create a new user and set her privileges to only this database in order to run the scripts in the package correctly

```
mysql> create database powertac_weather;
mysql> CREATE USER 'powertac'@'localhost' IDENTIFIED BY 'password';
mysql> GRANT ALL PRIVILEGES ON powertac_weather. * TO 'powertac'@'localhost';
mysql> FLUSH PRIVILEGES;
mysql> SHOW GRANTS username;
```


#### Setting up the data:

  1. To Run create weather table script
  	- if you've followd the steps above there's no need to populate/adjust the DB_user, DB_pass values, otherwise you should check those 
  	- check the tables are created, either from workbench or from cmd line 

 ```
    $python create-weather-tables.py
    $mysql 
    mysql> show databases;
    mysql> use powertac_weather;
    mysql> show tables;
  ```

  2. Run import knmi data script

  ```
    $python import_knmi_data.py
  ```


  3. Check if all reports are imported for the given location and period by running the below script.
     Alternatively, check directly using the query saved in verify reports table sql from command line or using the workbench interface 

  ```
  $python verify_weather_data.py
  ```
  
  
  4. Create forecast data and check it exists 
  
  ```
  $python create_forecast_data.py
  $python create_forecast_deltas.py
  #python verify_forecast_data.py 
  ```

#### Running the server
If you don't have a tomcat server configured, download a copy of apache tomcat 7(http://tomcat.apache.org).

* useful [link to set up tomcat on Mac Mojave](https://tonnygaric.com/blog/how-to-install-apache-tomcat-on-macos-10-14-mojave)

* Run the ./startup.sh script for apache tomcat 
`/Library/Tomcat/bin/startup.sh`

* Copy the example config files, and edit the properties if needed.
  Usually only db user/pass and the file locations are needed
  $cp weatherserver.properties.template         weatherserver.properties

* Run `mvn compile tomcat7:deploy` to deploy to tomcat.
  If needed change the username/password in pom.xml.
  
  Point to http://localhost:8080/WeatherServer to view 
  
Note:

* If you get  BUILD FAILURE due to broken pipe, i.e. 

Failed to execute goal org.apache.tomcat.maven:tomcat7-maven-plugin:2.2:deploy (default-cli) on project WeatherServer: Cannot invoke Tomcat manager: Broken pipe (Write failed) -> [Help 1]

Add the following to tomcat-users.xml. Explained [here](https://stackoverflow.com/questions/33918457/tomcat-7-maven-plugin-i-o-exception-java-net-socketexception-caught-when-pro)

```
<role rolename="manager-gui"/>
<role rolename="manager-script"/>
<role rolename="manager-jmx"/>
<role rolename="manager-status"/>
<user username="test1" password="test" roles="manager-script,manager-jmx" />
```

* If you get a "Connections could not be acquired from the underlying database!" message when requesting weather data 

i.e. http://localhost:8080/WeatherServer/faces/index.xhtml?weatherDate=2010030102&weatherLocation=rotterdam

Go to the error logs /usr/local/apache-tomcat-7.0.92/logs/catalina.[date].log and search for the error message, after misspelling by mistake, found that autoReconnect property in Database.java on line 38 should be corrected with capital letters

`WARNING: com.mchange.v2.resourcepool.BasicResourcePool$AcquireTask@3aeec608 -- Acquisition Attempt Failed!!! Clearing pending acquires. While trying to acquire a needed new resource, we failed to succeed more than the maximum number of allowed acquisition attempts (30). Last acquisition attempt exception: 
java.sql.SQLException: The connection property 'autoReconnect' acceptable values are: 'TRUE', 'FALSE', 'YES' or 'NO'. The value 'tru' is not acceptable.`


now the REST call on the Weather Server returns the xml we need.

#### Generate xml weather simulation data 
Run the simulation script passing the start date which can be seen in the server start page. This will produce a weather.xml file in the same directory
 
```
$python3 create_sim_weather.py 20100101
```
### Add more weather data
 Update the database tables and add the new location name to the publicLocations field in weatherserver.properties
 

