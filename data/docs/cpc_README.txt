			NCEP/CPC 4km Global (60N - 60S) IR Dataset
			---- --- --- ------  ---------- -- ------- 
I.  BACKGROUND

The Climate Prediction Center/NCEP/NWS is now making available via anonymous ftp (in
digital form) globally-merged (60N-60S) pixel-resolution IR brightness temperature
data (equivalent blackbody temps), merged from all available geostationary satellites
(GOES-8/10, METEOSAT-7/5 & GMS).  The availability of data from METEOSAT-7, which is
located at 57E at the present time, yields a unique opportunity for total global
(60N-60S) coverage.

The global IR composites available are now available in digital form for every 1/2
hour via a weekly rotating file.  The data have been corrected for "zenith angle
dependence", i.e. IR temperatures for locations far from satellite nadir are
erroneously cold due to a combination of geometric effects and radiometric path
extinction effects.  This correction allows for the merging of the IR data from the
various geostationary satellites with greatly reduced discontinuities at their
boundaries.  Some residual differences among the data exist since the IR channels
aboard the various spacecraft have slightly different characteristics and no
intercalibration among the sensors has been performed.  We are in the process of
performing such an intercalibration, although this effect is considerably smaller
than the zenith angle effects.

The data availability are delayed by 2 days from real-time to abide by international
data exchange agreements between NOAA and EUMETSAT (the METEOSAT data providers). We
are working on a web page that will have an image browse capability (at reduced
resolution) along with tools to make data downloading easier.

The data are too voluminous (33 MB per 1/2 hour) to service requests for historical data
or spatial subsets of the data.  However, the National Climatic Data Center (NCDC) has
agreed to be the official archive & distribution center for these data, although the
infrastructure for this activity is not yet in place.

Please note that, at present, we are using a makeshift assortment of existing in-house
hardware to perform these tasks and, while reliable over the course of the past few
months, is not optimal for the tasks at hand.  We are in the process of procuring a
dedicated system for this activity which should be installed within the next 2-3 months.

	
     *********************************************************************************
     *                                                                               *
     * 	This work is supported by funding from the NOAA Office of Global Programs    *
     *  for the Global Precipitation Climatology Project (GPCP and by NASA via the   *
     *	Tropical Rainfall Measuring Mission (TRMM).                                  *
     *                                                                               *
     *********************************************************************************
					


II.  DATA STRUCTURE
					
The "4 km" global (60N - 60S) merged IR data exist on a rectangular lat/lon grid. 
Each file contains 2 records: the 1st for the "on the hour" images (":00") and the 2nd for
the "on the half hour" images (":30"). The data & time of each file is determined by the
filename: merg_yyyymmddhh_4km-pixel, where

yyyy = year        mm = month         dd = day       hh = hour

Each record is a 9896 x 3298 Fortran array of IR brightness temperatures that have
been scaled to fit into 1-byte by subtracting "75" from each datum.  Therefore it
is necessary for the user to add a value of "75" to each data value when using the
data.

The orientation of the data in the array is EASTward from 0.0182E (center of
gridbox) and the grid increment in the east-west direction is 0.036378335 degrees
of longitude.  The data proceed from North -> South beginning at 59.982N (center of
gridbox) and the grid increment is 0.036383683 degrees of latitude in the
north-sout direction.  For GrADS users, the following ".ctl" file will be useful:


			DSET merg_1999042012_4km-pixel
			OPTIONS yrev little_endian template
			UNDEF  330
			TITLE  globally merged IR data
			XDEF 9896 LINEAR   0.0182 0.036378335
			YDEF 3298 LINEAR   -59.982 0.036383683
			ZDEF   01 LEVELS 1
			TDEF 99999  LINEAR   12z04Apr1999 30mn
			VARS 1
			ch4  1  -1,40,1,-1 IR BT  (add  '75' to this value)
			ENDVARS 

The original ("raw") data for the GOES 12 & 11, MT-SAT, METEOSAT 9 & 7 were obtained via the
McIDAS system, remapped to lat/lon gridded files & merged to form a global dataset.  
A zenith angle correction has been applied to the data to correct for
erroneously cold IR temperatures for locations that are far from the satellite
nadir position.  At present no intercalibration correction has been applied to the
data.

The beginning scan times for each satellite, in terms of minutes after the hour, are 
as shown below.  ":00" column refers to hour +  0 minutes; 
		 ":30"    "      "   to hour + 30 minutes

	Satellite				:00			:30
	---------				----			----
	
	GMS (centered @ 140E longitude)		57			30
	
	**GOES-12 (east; 75W)			45			15
	
	**GOES-11 (west; 135W)			00			30
	
	Meteosat-9 (Greenwich)			00			30
	
	Meteosat-7 (57E longitude)		00			30
	
		** GOES full-disc views are guaranteed only at 00Z, 03Z, ..., 21Z.  For
			images NOT at these time, the GOES data may be assembled
			from various regioinal subsets of a full-disc view due to 
			image scheduling of the GOES satellites.
	
  --------------------------------------------------------------------------------------

	Note 1.  Due to the voluminous nature of these data, historical data
	cannot  be provided.

	Note 2.  IR data from the various geostationary satellites are not scanned 
	at exactly the same time.  

	Note 3.  While the nominal spatial resolution is 4 km, the data at
	locations  far from nadir are considerably less resolved.  Functionally,
	the data at such locations is essentially repeated among adjacent
	gridboxes.

	Note 4.  At present, no intersatellite calibration has been performed on
	these  data.  

	Note 5.  Full-disc images from GOES are guaranteed every 3 hrs only (00Z,
	03Z, ... 21Z).  At the non-3hr times, various subsets of GOES views are
	acquired and pieced together for the global product.  This is the reason for
	relatively frequent missing data in the GOES domain. 
  --------------------------------------------------------------------------------------

For more information contact:  John Janowiak (jjanowia@umd.edu) or

				Bob Joyce (robert.joyce@noaa.gov)
