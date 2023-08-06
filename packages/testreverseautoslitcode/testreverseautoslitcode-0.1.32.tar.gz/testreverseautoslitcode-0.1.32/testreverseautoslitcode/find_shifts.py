#code to query GAIA(or PanSTARRS or Custom) database for closest object to calculated coordinates

#import packages
import numpy as np
from astropy.coordinates import SkyCoord, ICRS, Galactic, FK4, FK5
import astropy.units as u
from astroquery.gaia import Gaia
from astroquery.mast import Catalogs
from astropy.table import Table,Column

def get_shift(data,theta,catalog_keyword,output_file,ref_system,racenter,deccenter,filename,maskbluID,adcuse):
    #Set up arrays and columns to hold results
    rpd = np.pi/180.  #radians per degree
    ra_shifts=[]
    dec_shifts = []
    ra_centers = []
    dec_centers = []
    x_centers = []
    y_centers = []
    catalog_obj_ra = []
    catalog_obj_dec = []
    objects_ra = []
    objects_dec = []
    data.add_column(0.00000000000,name='RA_Center')
    data.add_column(0.00000000000,name='Dec_Center')
    data.add_column(0.00000000000,name='X_Center')
    data.add_column(0.00000000000,name='Y_Center')
    data.add_column(0.00000000000,name='Cat_Obj_RA')
    data.add_column(0.00000000000,name='Cat_Obj_Dec')

    #Step through each slit and calcuate the center of each one by averaging
    i=0
    k =0
    print('--------------Querying Catalog-------------')
    while i <= len(data)-4:
        #Load in the corners for a given slit in both RA,Dec and x,y and calculate the ratio of the sides
        ra1,ra2,ra3,ra4 = data['Calc_RA'][i],data['Calc_RA'][i+1],data['Calc_RA'][i+2],data['Calc_RA'][i+3]
        dec1,dec2,dec3,dec4 = data['Calc_Dec'][i],data['Calc_Dec'][i+1],data['Calc_Dec'][i+2],data['Calc_Dec'][i+3]
        side1 = 3600*np.sqrt(((ra2-ra1)*np.cos(dec1*np.pi/180))**2+(dec1-dec2)**2)
        side2 = 3600*np.sqrt(((ra2-ra3)*np.cos(dec2*np.pi/180))**2+(dec3-dec2)**2)
        ratio = side1/side2
        ra_arr=[ra1,ra2,ra3,ra4]
        dec_arr=[dec1,dec2,dec3,dec4]
        ra_avg = (np.max(ra_arr)+np.min(ra_arr))/2.
        dec_avg = (np.max(dec_arr)+np.min(dec_arr))/2.
        xpos = [data['X'][i],data['X'][i+1],data['X'][i+2],data['X'][i+3]]
        ypos = [data['Y'][i],data['Y'][i+1],data['Y'][i+2],data['Y'][i+3]]
        x_avg = (np.max(xpos)+np.min(xpos))/2.
        y_avg = (np.max(ypos)+np.min(ypos))/2.
        data['RA_Center'][i],data['RA_Center'][i+1],data['RA_Center'][i+2],data['RA_Center'][i+3]=ra_avg,ra_avg,ra_avg,ra_avg
        data['Dec_Center'][i],data['Dec_Center'][i+1],data['Dec_Center'][i+2],data['Dec_Center'][i+3]=dec_avg,dec_avg,dec_avg,dec_avg
        data['X_Center'][i],data['X_Center'][i+1],data['X_Center'][i+2],data['X_Center'][i+3]=x_avg,x_avg,x_avg,x_avg
        data['Y_Center'][i],data['Y_Center'][i+1],data['Y_Center'][i+2],data['Y_Center'][i+3]=y_avg,y_avg,y_avg,y_avg
#=================================================================================================================================
        #decide if current slit is an alignment box based on the ratio of the lengths of the sides of the slits
        if 0.95 < ratio < 1.05:
            k=k+1
            ra_centers.append(ra_avg)
            dec_centers.append(dec_avg)
            x_centers.append(x_avg)
            y_centers.append(y_avg)
            print('ra,dec of box =',ra_avg,dec_avg)

#=================================================================================================================================
            #call astroquery with the chosen catalog to gather list of objects in and near the alignment boxes

            coord = SkyCoord(ra=ra_avg, dec=dec_avg, unit=(u.deg,u.deg),frame=ref_system)
            if catalog_keyword == 'gaia':
                width = 200*u.arcsec
                height = 200*u.arcsec
                obj = Gaia.query_object_async(coordinate=coord, width=width,height=height)
                mag_cutoff = (obj['phot_g_mean_flux']>18.)
                obj = obj[mag_cutoff]

                objects_ra.append(obj['ra'])
                objects_dec.append(obj['dec'])

                objects_ra.append(obj['ra'])
                objects_dec.append(obj['dec'])

                #find the object with the closest position
                diff = []
                for j in range(len(obj)):
                    diff.append(np.sqrt(((obj['ra'][j]-ra_avg)*np.cos(dec_avg*np.pi/180.))**2+(obj['dec'][j]-dec_avg)**2))
                min_diff = np.argmin(diff)

                #save catalog object to array
                catalog_obj_ra.append(obj[min_diff]['ra'])
                catalog_obj_dec.append(obj[min_diff]['dec'])

                data['Cat_Obj_RA'][i],data['Cat_Obj_RA'][i+1],data['Cat_Obj_RA'][i+2],data['Cat_Obj_RA'][i+3] = obj[min_diff]['ra'],obj[min_diff]['ra'],obj[min_diff]['ra'],obj[min_diff]['ra']
                data['Cat_Obj_Dec'][i],data['Cat_Obj_Dec'][i+1],data['Cat_Obj_Dec'][i+2],data['Cat_Obj_Dec'][i+3] = obj[min_diff]['dec'],obj[min_diff]['dec'],obj[min_diff]['dec'],obj[min_diff]['dec']

                print('GAIA object located at:',obj[min_diff]['ra'],obj[min_diff]['dec'])
                ra_shifts.append((ra_avg-obj['ra'][min_diff])*np.cos(dec_avg*np.pi/180.))
                dec_shifts.append(dec_avg-obj['dec'][min_diff])

            if catalog_keyword == 'panstarrs':
                obj = Catalogs.query_region(coord, radius=15*u.arcsec, catalog='Panstarrs', data_release='dr2')
               # mag_cutoff = (obj['gMeanKronMag']>18.)
                #obj = obj[mag_cutoff]

                objects_ra.append(obj['raMean'])
                objects_dec.append(obj['decMean'])


                #find the object with the closest position
                diff = []
                for j in range(len(obj)):
                    diff.append(np.sqrt(((obj['raMean'][j]-ra_avg)*np.cos(dec_avg*np.pi/180.))**2+(obj['decMean'][j]-dec_avg)**2))
                min_diff = np.argmin(diff)


                #save catalog object to array
                catalog_obj_ra.append(obj[min_diff]['raMean'])
                catalog_obj_dec.append(obj[min_diff]['decMean'])

                data['Cat_Obj_RA'][i],data['Cat_Obj_RA'][i+1],data['Cat_Obj_RA'][i+2],data['Cat_Obj_RA'][i+3] = obj[min_diff]['raMean'],obj[min_diff]['raMean'],obj[min_diff]['raMean'],obj[min_diff]['raMean']
                data['Cat_Obj_Dec'][i],data['Cat_Obj_Dec'][i+1],data['Cat_Obj_Dec'][i+2],data['Cat_Obj_Dec'][i+3] = obj[min_diff]['decMean'],obj[min_diff]['decMean'],obj[min_diff]['decMean'],obj[min_diff]['decMean']

                print('PANSTARRS object located at:',obj[min_diff]['raMean'],obj[min_diff]['decMean'])
                ra_shifts.append((ra_avg-obj['raMean'][min_diff])*np.cos(dec_avg*np.pi/180.))
                dec_shifts.append(dec_avg-obj['decMean'][min_diff])

            if catalog_keyword == 'custom':
                obj = Table.read(filename)
                objects_ra.append(obj['ra'])
                objects_dec.append(obj['dec'])

                #find the object with the closest position
                diff = []
                for j in range(len(obj)):
                    diff.append(np.sqrt(((obj['ra'][j]-ra_avg)*np.cos(dec_avg*np.pi/180.))**2+(obj['dec'][j]-dec_avg)**2))
                min_diff = np.argmin(diff)

                #save catalog object to array
                catalog_obj_ra.append(obj[min_diff]['ra'])
                catalog_obj_dec.append(obj[min_diff]['dec'])

                data['Cat_Obj_RA'][i],data['Cat_Obj_RA'][i+1],data['Cat_Obj_RA'][i+2],data['Cat_Obj_RA'][i+3] = obj[min_diff]['ra'],obj[min_diff]['ra'],obj[min_diff]['ra'],obj[min_diff]['ra']
                data['Cat_Obj_Dec'][i],data['Cat_Obj_Dec'][i+1],data['Cat_Obj_Dec'][i+2],data['Cat_Obj_Dec'][i+3] = obj[min_diff]['dec'],obj[min_diff]['dec'],obj[min_diff]['dec'],obj[min_diff]['dec']

                print('Custom object located at:',obj[min_diff]['ra'],obj[min_diff]['dec'])
                ra_shifts.append((ra_avg-obj['ra'][min_diff])*np.cos(dec_avg*np.pi/180.))
                dec_shifts.append(dec_avg-obj['dec'][min_diff])

            i=i+4
        else:
            i=i+4
#=================================================================================================================================
#Because we are not sure if the catalog object matched with each box is the correct one, we determine which shifts are likely due to correct objects
#being matched to the boxes (ie. "good" shifts). This is done by determining whether the shift array contains both "small" and "large" shift values (as
#defined by cutoff values). If this is the case, the outliers are found by removing the small/large values by determining which the shift array has more
#of and removing the small/large values that the array has fewer of.

    good_ra_shifts=[]
    good_dec_shifts=[]
    removed = 0
    large = 0
    small = 0
    if (np.min(np.abs(ra_shifts))*3600 < 1.2 and np.max(np.abs(ra_shifts))*3600 > 5.0) or (np.min(np.abs(dec_shifts))*3600 < 1.2 and np.max(np.abs(dec_shifts))*3600 > 5.0):
        print('Found Outliers...')
        for h in range(len(ra_shifts)):
            if np.abs(ra_shifts[h])*3600 < 1.2 and np.abs(dec_shifts[h])*3600 < 1.2:
                small = small +1
            else:
                large = large+1
        if small >= large:
            for n in range(len(ra_shifts)):
                if np.abs(ra_shifts[n])*3600 > 5. or np.abs(dec_shifts[n])*3600 > 5.0:
                    removed = removed +1
                    n=n+1
                else:
                    good_ra_shifts.append(ra_shifts[n])
                    good_dec_shifts.append(dec_shifts[n])
        if large > small:
            for n in range(len(ra_shifts)):
                if np.abs(ra_shifts[n])*3600 < 5. or np.abs(dec_shifts[n])*3600 < 5.0:
                    removed = removed +1
                    n=n+1
                else:
                    good_ra_shifts.append(ra_shifts[n])
                    good_dec_shifts.append(dec_shifts[n])
    else:
        good_ra_shifts = ra_shifts
        good_dec_shifts = dec_shifts

    print(small,'small shifts')
    print(removed,'elements removed from shift arrays')
#=================================================================================================================================
#Calculate the final shifts to apply to the slit positions by averaging the individual "good" shifts from the boxes.
    dec_shift_final = np.average(good_dec_shifts)
    ra_shift_final = np.average(good_ra_shifts)/np.cos(data['Calc_Dec'][0]*np.pi/180)
    final_shifts = np.zeros(len(good_ra_shifts))
    for g in range(len(final_shifts)):
        final_shifts[g] = np.sqrt((good_ra_shifts[g]/np.cos(data['Calc_Dec'][0]*np.pi/180))**2+(good_dec_shifts[g]**2))*3600
    total_shift_final = np.sqrt(ra_shift_final**2+dec_shift_final**2)*3600
    total_shift_dispersion =np.sqrt(np.sum((final_shifts-total_shift_final)**2)/(len(final_shifts)-1))

#Determine whether or not to apply a shift. If the total dispersion value for the shift is too large, or is above 0.7 times the shift values
#do not apply a shift.
    if total_shift_dispersion >=2.0 or np.isnan(total_shift_final) == True:
        ra_shift_final = np.float64(0.0)
        dec_shift_final = np.float64(0.0)
        print('---------No Systematic Shift Found. No Shift Applied---------')
    if 0.70 < total_shift_dispersion/total_shift_final:
        ra_shift_final = np.float64(0.0)
        dec_shift_final = np.float64(0.0)
        print('---------No Systematic Shift Found. No Shift Applied---------')

    ra_shifted_centers = ra_centers-ra_shift_final
    dec_shifted_centers = dec_centers-dec_shift_final
    print('Final Shift:',str(round(total_shift_final,3))+'+/-'+str(round(total_shift_dispersion,3)))


    ra_shifted_centers = ra_centers-ra_shift_final
    dec_shifted_centers = dec_centers-dec_shift_final

#=================================================================================================================================
#Calculate the difference between the shifted centers and the catalog objects
    after_shifts_total = np.zeros(len(ra_centers))
    before_shifts_total = np.zeros(len(ra_centers))
    after_ra_shifts = np.zeros(len(ra_centers))
    before_ra_shifts = ra_shifts
    for g in range(len(after_shifts_total)):
        before_ra_diff = 3600*(ra_centers[g] - catalog_obj_ra[g])*np.cos(data['Calc_Dec'][0]*np.pi/180)
        before_dec_diff = 3600*(dec_centers[g] - catalog_obj_dec[g])
        ra_diff = 3600*(ra_shifted_centers[g] - catalog_obj_ra[g])*np.cos(data['Calc_Dec'][0]*np.pi/180)
        after_ra_shifts[g]=ra_diff
        before_ra_shifts[g] = 3600.*ra_shifts[g]
        dec_diff = 3600*(dec_shifted_centers[g] - catalog_obj_dec[g])
        before_shifts_total[g] = np.sqrt((before_ra_diff)**2+(before_dec_diff)**2)
        after_shifts_total[g] = np.sqrt((ra_diff)**2+(dec_diff)**2)
    print('Before Shifts:',before_shifts_total)
    print('After Shifts:',after_shifts_total)
    print('Before RA Shifts:',before_ra_shifts)
    print('After RA Shifts:',after_ra_shifts)
#=================================================================================================================================
#Shift the slit positions
    data['Calc_RA'] = data['Calc_RA']-ra_shift_final
    data['Calc_Dec'] = data['Calc_Dec']-dec_shift_final
    data['RA_Center'] = data['RA_Center']-ra_shift_final
    data['Dec_Center'] = data['Dec_Center']-dec_shift_final

    return(data,x_centers,y_centers,ra_shifted_centers,dec_shifted_centers,catalog_obj_ra,catalog_obj_dec,objects_ra,objects_dec)
