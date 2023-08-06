from data_downloader import downloader
import os

urls = ['http://gws-access.jasmin.ac.uk/public/nceo_geohazards/LiCSAR_products/106/106D_05049_131313/metadata/106D_05049_131313.geo.E.tif',
        'http://gws-access.jasmin.ac.uk/public/nceo_geohazards/LiCSAR_products/106/106D_05049_131313/metadata/106D_05049_131313.geo.N.tif',
        'http://gws-access.jasmin.ac.uk/public/nceo_geohazards/LiCSAR_products/106/106D_05049_131313/metadata/106D_05049_131313.geo.U.tif',
        'http://gws-access.jasmin.ac.uk/public/nceo_geohazards/LiCSAR_products/106/106D_05049_131313/metadata/106D_05049_131313.geo.hgt.tif',
        'http://gws-access.jasmin.ac.uk/public/nceo_geohazards/LiCSAR_products/106/106D_05049_131313/metadata/baselines',
        'http://gws-access.jasmin.ac.uk/public/nceo_geohazards/LiCSAR_products/106/106D_05049_131313/metadata/metadata.txt']


downloader.async_download_datas(urls, '/media/fanchy/data/Github/temp')
