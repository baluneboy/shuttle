# shuttle python repository
Read and display Space Shuttle vibratory acceleration data.  Demo code plots spectrogram of crew sleep-to-wake transition.

## Space Acceleration Measurement System (SAMS) on USMP-4 (STS-87) Launched in 1997

*See summary report [here](https://pims.grc.nasa.gov/plots/user/pims/reports/Summary_Report_of_Mission_Acceleration_STS-87_USMP-4_1997.pdf).*

*Download 1st 4 days of SAMS data from NASA public web server [here](https://pims.grc.nasa.gov/ftp/usmp4/).*

| SAMS Sensor   | Fs (sa/sec) | Fc (Hz)  | Location                             |
| ------------- | -----------:| --------:| :------------------------------------|
| Unit F, TSH A | 50          | 10       | Forward MPESS Carrier (Near AADSF)   |
| Unit F, TSH B | 125         | 25       | Forward MPESS Carrier (Near MEPHISTO)|
| Unit G, TSH A | 50          | 5        | Rear MPESS Carrier (Inside IDGE)     |
| Unit G, TSH B | 250         | 100      | Rear MPESS Carrier (Inside CHeX)     |

### Crew Sleep
*See Table 17 on p. 19 of summary report [here](https://pims.grc.nasa.gov/plots/user/pims/reports/Summary_Report_of_Mission_Acceleration_STS-87_USMP-4_1997.pdf#page=30).*

Run demo.py to get results like what is shown below (without the red annotations).

![crew wake example image](/screenshot.png?raw=true "Crew Wake Example")
