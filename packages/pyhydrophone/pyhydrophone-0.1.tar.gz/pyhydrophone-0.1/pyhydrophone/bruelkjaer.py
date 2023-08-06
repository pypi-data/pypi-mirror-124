#!/usr/bin/python
"""
Module : bruelkjaer.py
Authors : Clea Parcerisas
Institution : VLIZ (Vlaams Instituut voor de Zee)
Last Accessed : 9/23/2020
"""

from pyhydrophone.hydrophone import Hydrophone

import os
import numpy as np
import soundfile as sf
import datetime


class BruelKjaer(Hydrophone):
    def __init__(self, name, model, serial_number, amplif, Vpp=2.0, string_format="%y%m%d%H%M%S", type_signal='ref'):
        """
        Init an instance of B&K Nexus.
        Check well the Vpp in case you don't have a reference signal! Specially of the recorder used.
        Parameters
        ----------
        name: str
            Name of the acoustic recorder
        model: str or int
            Model of the acoustic recorder
        serial_number : str or int
            Serial number of the acoustic recorder
        amplif: float
            Amplification selected in the Nexus in V/Pa
        Vpp: float
            Volts peak to peak
        string_format: string
            Format of the datetime string present in the filename
        type_signal : str
            Can be 'ref' or 'test'
        """
        if amplif not in [100e-6, 316e-6, 1e-3, 3.16e-3, 10e-3, 31.6e-3, 100e-3, 316e-3, 1.0, 3.16, 10.0]:
            raise Exception('This amplification is not available!')
        self.amplif = amplif
        self.type_signal = type_signal
        sensitivity = 10 * np.log10((self.amplif/1e6)**2)
        
        # preamp is considered 0 beacause all the conversion is done as an end-to-end in the reference signal
        super().__init__(name, model, serial_number, sensitivity=sensitivity, preamp_gain=0.0,
                         Vpp=Vpp, string_format=string_format)

    def __setattr__(self, name, value):
        """
        If the amplif is changed, update the pream_gain
        """
        if name == 'amplif':
            self.__dict__['sensitivity'] = 10 * np.log10((value/1e6)**2)
        if name == 'type_signal':
            if value not in ['ref', 'test']:
                raise Exception('%s is not an option in Nexus!' % value)
        return super().__setattr__(name, value)

    def get_name_datetime(self, file_name, utc=False):
        """
        Get the data and time of recording from the name of the file
        Parameters
        ----------
        file_name : string
            File name (not path) of the file
        utc : boolean
            If set to True, the time of the file will be considered Local and will be changed to utc according to
            the computer timezone
        """
        name = file_name.split('.')
        date_string = name[0].split('_')[0]
        date = super().get_name_datetime(date_string, utc=utc)
        return date

    def get_new_name(self, filename, new_date):
        """
        Replace the datetime with the appropriate one
        Parameters
        ----------
        filename : string
            File name (not path) of the file
        new_date : datetime object
            New datetime to be replaced in the filename
        """
        old_date = self.get_name_datetime(filename)
        old_date_name = datetime.datetime.strftime(old_date, self.string_format)
        new_date_name = datetime.datetime.strftime(new_date, self.string_format)
        new_filename = filename.replace(old_date_name, new_date_name)
        
        return new_filename

    def read_start_time_metadata(self, file_path, utc=False):
        """
        Return the starting time of the file by getting the last modification minus the duration of the file
        Parameters
        ----------
        file_path : string or Path
            Path to the file to read the information from
        utc : boolean
            If set to True, the time of the file will be considered Local and will be changed to utc according to
            the computer timezone

        Returns
        -------
        Datetime, starting moment of the file
        """
        modif_timestamp = os.path.getmtime(file_path)
        modif_datetime = datetime.datetime.fromtimestamp(modif_timestamp)
        duration = datetime.timedelta(seconds=sf.info(file_path).duration)
        start_time = modif_datetime - duration
        if utc:
            timeoff = datetime.datetime.utcnow() - datetime.datetime.now()
            start_time += timeoff
        return start_time
    
    def update_calibration(self, ref_signal):
        """
        Update the calibration
        Parameters
        ----------
        ref_signal : str or Path
            File path to the reference file to update the Vpp according to the calibration tone
        """
        ref_wav = np.sqrt((ref_signal ** 2).mean())
        # Sensitivity is in negative values!
        if self.type_signal == 'ref':
            # The signal is then 1 V
            ref_v = 1
        else:
            # The signal is the amplification value
            ref_v = 100 * self.amplif * np.sqrt(2)
        self.sensitivity = 10 * np.log10((self.amplif / 1e6) ** 2) + 10*np.log10((ref_wav / ref_v)**2)
