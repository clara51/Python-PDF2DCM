import os

from pynetdicom import AE, VerificationPresentationContexts, evt, StoragePresentationContexts

store_path = '/path'


def handler_store(event):
    ds = event.dataset
    ds.file_meta = event.file_meta
    # ds.SamplesPerPixel = 3
    ds.save_as(os.path.join(store_path, ds.SOPInstanceUID + '.dcm'), write_like_original=True)

    return 0x0000


handlers = [(evt.EVT_C_STORE, handler_store)]

ae = AE()

ae.supported_contexts = StoragePresentationContexts

ae.start_server(('127.0.0.1', 11112), evt_handlers=handlers)
