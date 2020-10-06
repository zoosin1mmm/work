    resp = requests.put(HOST, headers={"Content-Type": "application/json; charset=utf-8"}, json=data)
    resp = requests.put(url=HOST ,headers={"Content-Type": "application/json; charset=utf-8"},data=data)
    req = requests.request(method='PUT',url=HOST ,headers={"Content-Type": "application/json; charset=utf-8"},json=data)
    print req

    req = requests.Request(method='PUT',url=HOST ,headers={"Content-Type": "application/json; charset=utf-8"},auth=(VALID_USER,VALID_PASSWORD),json=data)
    preq = req.prepare()
    session = requests.Session()
    resp = session.send(preq)
    print resp

    print "Create owner user ..."
    time.sleep(5)
    ownerEmail = "testing+%s+semi+vert@exosite.com" % time.strftime("%Y%m%d%H%M%S")
    ownerPassword = ownerEmail
    HOST = "https://%s.%s/api:1" % (solutionName, SOLUTION_HOST)
    print "https://%s.%s/api:1/user/%s" % (solutionName, SOLUTION_HOST,ownerEmail)
    resp = ExoUserEmail().user_email_put(ownerEmail,ownerPassword,HOST)
    print resp
    ExoFileLibrary().inplace_change(setting_dir, 'OWNER_EMAIL = "testing+semi+vert@exosite.com"', "OWNER_EMAIL = \"{}\"".format(ownerEmail))
    ExoFileLibrary().inplace_change(setting_dir, 'OWNER_PASSWORD = "testing+semi+vert@exosite.com"', "OWNER_PASSWORD = \"{}\"".format(ownerPassword))

    print "Create guest user ..."
    guestEmail = "testing+%s+guest+semi@exosite.com" % time.strftime("%Y%m%d%H%M%S")
    guestPassword = guestEmail
    print 'start'
    resp = ExoUserEmail().user_email_put(guestEmail,guestPassword)
    print resp
    ExoFileLibrary().inplace_change(setting_dir, 'GUEST_EMAIL = "testing+guest+semi@exosite.com"', "GUEST_EMAIL = \"{}\"".format(guestEmail))
    ExoFileLibrary().inplace_change(setting_dir, 'GUEST_PASSWORD = "testing+guest+semi@exosite.com"', "GUEST_PASSWORD = \"{}\"".format(guestPassword))
    

     print "Create owner user ..."
    time.sleep(5)
    ownerEmail = "testing+%s+semi+vert@exosite.com" % time.strftime("%Y%m%d%H%M%S")
    ownerPassword = ownerEmail
    data = {"password":"%s" % ownerPassword}
    data = json.dumps(data)
    HOST = "https://%s.%s/api:1/user/%s" % (solutionName, SOLUTION_HOST,ownerEmail)
    print HOST
    print "set Session"
    curl=requests.Session()
    curl.headers.update({
            "Content-Type": "application/json; charset=utf-8",
        })
    print "Put request"
    resp = curl.request(method='PUT',url=HOST ,json=data)
    print resp
    ExoFileLibrary().inplace_change(setting_dir, 'OWNER_EMAIL = "testing+semi+vert@exosite.com"', "OWNER_EMAIL = \"{}\"".format(ownerEmail))
    ExoFileLibrary().inplace_change(setting_dir, 'OWNER_PASSWORD = "testing+semi+vert@exosite.com"', "OWNER_PASSWORD = \"{}\"".format(ownerPassword))
