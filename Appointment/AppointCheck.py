import requests

if __name__ == '__main__':
    token = None
    api = "https://cvp1.moph.go.th/api/appointment/AppointmentSlot?Action=GetHospitalSlotConfirmByDate&hospital_code=00051&date=2024-05-02"
    params = {

    }
    with open("../token.txt") as f:
        token = f.read()

    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(api, params=params, headers=headers)
    print(r.json())
