from argentina.economia import ipc_nacional, emae, tipo_cambio_minorista

ipc = ipc_nacional(start_date="2020-01-01")
emae_df = emae(start_date="2020-01-01")
tc = tipo_cambio_minorista(start_date="2020-01-01")

print(ipc.head())
print(emae_df.head())
print(tc.head())
