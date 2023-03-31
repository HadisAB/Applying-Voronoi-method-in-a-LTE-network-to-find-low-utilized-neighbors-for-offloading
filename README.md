# Applying-Voronoi-method-in-a-LTE-network-to-find-low-utilized-neighbors-for-offloading
This project is supposed to check the neighbors of congested LTE cells (which are detected by applying Voronoi method) to find if it is possible to offload them on their low utilized neighbors. 
## Goal
Growing the number of LTE users leads to site congestion in the network. In this project we are going to find the congested cells and check their exact neighbors status to check if it is possible to offload the payload on them by changing the planning parameters such as E_tilt, M-tilt or Azimuth. <br /> 
Finding the geographical sector neighbors in the cellular network is the main challange of this project. Because the neighbors in 2G and 3G are defined manually and consist of all sites around the coverage area while we need the ones which are located in the direction of each sector.<br />
Although the neighbors are defined automatically in 4G, the number of neighbors in ANR are a lot (even the overshooting cases exist in the ANR list), So it is not useful for our report, too. 

## Solution
To cope with the mentioned problems we used  **‘Voronoi’** method to find the neighbors and checking the usage between them.<br />


## Voronoi
A Voronoi diagram is a mathematical diagram that divides a plane into areas that are close to each of a given set of objects.
The method has been applied to all sectors in the country to find the list of neighbors who can be candidates to off load on them by changing azimuth or tilt.<br /><br />
<img src=https://github.com/HadisAB/Applying-Voronoi-method-in-a-LTE-network-to-find-low-utilized-neighbors-for-offloading/blob/main/Git_Capture.PNG width="300" height="240"/>

<br /><br />
## Method
The steps of used algorithm:<br />

1. Moving each sector in the direction of Azimuth to make it ready to be used in our Voronoi method.
2. Finding the neighbors in the area of each sector by applying Voronoi method.
3. Extending the method to cell level. 
4. Checking the utilization of each cell and its neighbors based on below criteria
    * Congested cells are the cells with more than 70% daily PRB_Utilization_Rate.
    * Candidates are the cells with less than 30% daily PRB_Utilization_Rate with the location of which is also  3km far from congested cell.
5. The list of congested and candidates will be prepared in one excel to be shared with relevant teams. They need to check if it is possible to offload the payload by changing tilt or azimuth or not.   

## Scripts
This [project](https://github.com/HadisAB/Applying-Voronoi-method-in-a-LTE-network-to-find-low-utilized-neighbors-for-offloading/blob/main/Voronoi_Git.py) has been written by python programming language.<br />
The [inputs](https://github.com/HadisAB/Applying-Voronoi-method-in-a-LTE-network-to-find-low-utilized-neighbors-for-offloading/blob/main/Git_Input.rar) are CSV files consist of daily PRB_Utilization_Rate values for all cells in the network or desired area.<br />
In addition the geographical information of sites ('Sec', 'Azimuth', 'Latitude', 'Longitude') should be inserted as input.<br /><br />
The output consists of the list of congested cells and the low_utilized neighbors as condidates to off load on them by changing planning parameters such as Tilt or Azimuth. <br />

