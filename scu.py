from pydicom import dcmread
from pydicom._storage_sopclass_uids import CTImageStorage, MRImageStorage
from pydicom.uid import ImplicitVRLittleEndian
from pynetdicom import AE, VerificationPresentationContexts, StoragePresentationContexts

# from pynetdicom.sop_class import CTImageStorage, MRImageStorage

dcm_path = '/path/report_0.dcm'

ae = AE(ae_title=b'MY_STORAGE_SCU')

# ae.requested_contexts = VerificationPresentationContexts

# ae.requested_contexts = StoragePresentationContexts

# ae.add_requested_context(CTImageStorage, transfer_syntax=[ImplicitVRLittleEndian, '1.2.840.10008.1.2.1'])
ae.add_requested_context(MRImageStorage, transfer_syntax=['1.2.840.10008.1.2.2'])

assoc = ae.associate('127.0.0.1', 11112)
if assoc.is_established:
    dataset = dcmread(dcm_path)
    status = assoc.send_c_store(dataset)
    assoc.release()
    if status:
        # If the storage request succeeded this will be 0x0000
        print('C-STORE request status: 0x{0:04x}'.format(status.Status))
    else:
        print('Connection timed out, was aborted or received invalid response')

    assoc.release()
else:
    print('Association rejected, aborted or never connected')
