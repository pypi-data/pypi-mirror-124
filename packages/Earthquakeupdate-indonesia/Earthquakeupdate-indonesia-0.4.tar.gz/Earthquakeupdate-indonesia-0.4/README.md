# Indonesia Earthquake Monitoring
This package will receive the latest earthquake information from BMKG | Meteorological, Climatological, and Geophysical Agency

## HOW IT WORKS
This package will scrape form [BMKG](https:bmkg.go.id) to get latest information of earthquake in Indonesia

It utilizes Beautifulsoup4 and Requests to produce JSON output that is ready to be used in web or mobile applications

## HOW TO USE
```
import updategempa

if __name__ == '__main__' :
    print('Aplikasi utama')
    result = updategempa.ekstraksi_data()
    updategempa.tampilkan_data(result)
```

#Author
Vivi Rosita R