package org.powertac.weatherserver;

import org.powertac.weatherserver.beans.Location;

import javax.faces.bean.ManagedBean;
import javax.faces.bean.RequestScoped;
import java.util.ArrayList;
import java.util.List;

@ManagedBean
@RequestScoped
public class ActionIndex{
	
  public List<Location> locationList;
  
  public ActionIndex (){}

  public List<Location> getLocationList(){
    locationList = new ArrayList<Location>();
    try {
    	locationList = Location.getAvailableLocations();
    }
    catch (Exception e) {
      e.printStackTrace();
    }

    return locationList;
  }
  
  public void setLocationList(List<Location> locations ) {
	  locationList = locations;
  }

}
