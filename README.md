# Applying-Voronoi-method-in-a-LTE-network-to-find-low-utilized-neighbors-for-offloading
This project is supposed to check the neighbors of congested LTE cells (which are detected by applying Voronoi method) to find if it is possible to offload them on their low utilized neighbors. 
## Goal
Growing the number of LTE users leads to site congestion in the network. In this project we are going to find the congested cells and check their exact neighbors status to check if it is possible to offload the payload on them by changing the planning parameters such as E_tilt, M-tilt or Azimuth. 
Finding the geographical sector neighbors in the cellular network is the main challange of this project. Because the neighbors in 2G and 3G are defined manually and consist of all sites around the coverage area while we need the ones which are located in the direction of each sector.
Although the neighbors are defined automatically in 4G, the number of neighbors in ANR are a lot (even the overshooting cases exist in the ANR list), So it is not useful for our report, too. 
