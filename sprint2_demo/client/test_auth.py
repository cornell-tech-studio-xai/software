import quickstart
from oauth2client import client


auth_code = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImRhOWUzZDdjZGQxYjQxNzgwMTBmODlhZjExY2ZkMzc0MDAwNjFhZmMifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiaWF0IjoxNDc5MjY5OTM4LCJleHAiOjE0NzkyNzM1MzgsImF0X2hhc2giOiJSR0FyZi1ILWJ0S1ZzMldKYnBWN1lBIiwiYXVkIjoiOTkxNjE0NjMxMTExLWszdGw3anNyYXE2NzY3OWdrZ2FkY2k3ZG4xYnV1ampmLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA5NTM5ODEwODU1Nzc3MjAyMjkxIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF6cCI6Ijk5MTYxNDYzMTExMS1rM3RsN2pzcmFxNjc2Nzlna2dhZGNpN2RuMWJ1dWpqZi5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImVtYWlsIjoia2F2aW4yNDY4QGdtYWlsLmNvbSIsIm5hbWUiOiJFdmFuIEtlc3RlbiIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vLW1QZllxQk94LW0wL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FFTU9ZU0E5ZEZDM2xDOW5jVTg0alpTb3V6NVJmNjNNb2cvczk2LWMvcGhvdG8uanBnIiwiZ2l2ZW5fbmFtZSI6IkV2YW4iLCJmYW1pbHlfbmFtZSI6Iktlc3RlbiIsImxvY2FsZSI6ImVuIn0.u5QRYqgPSAbfS5joNMkJAReTymZ9u6Bee6RaxGzPR0x00Zab-lp0ahXuyGGqxUFH_E5s3OY7_dS2wuHhcur_vG-S0d5g4VovqE1tyxdQUCou8u2n-0WiVq4iQaWI2DQdxO8jKbsXg1iEdCWv39pU_9Z9YRiPPADddQ-Alzh3t8L8cuxscVl_dcb8_ZzCCxskrQujbh74_jUxeGLD7UnUPPRNo8KSEIbuxmLxhdXCGtmtU_x_hS3t-gTf3CycT6qNImHVK3bd4m5_sEM47bJaeR4GCv3PgTtsxWx8fQkFawG8ooCUJ7ZoxhJpzsHs3R4cZ7P7W3WZFIiQUkG0AQJexQ"
flow = client.flow_from_clientsecrets(
    'client_secret.json',
    scope="profile email https://www.googleapis.com/auth/gmail.readonly",
    redirect_uri='http://localhost:3000')
flow.redirect_uri = "http://localhost:3000"
flow.params['access_type'] = 'offline'
credentials = flow.step2_exchange(auth_code)