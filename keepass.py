from pywinauto.application import Application
from pywinauto.keyboard import SendKeys
from pywinauto import keyboard, clipboard
import time
import os

OUTPUT = 'output'
WORKDIR = os.getcwd()

if not os.path.isdir(os.path.join(os.getcwd(), OUTPUT)):
    os.makedirs(OUTPUT)


# Step 1: Open & Log into KeePass
app = Application(backend="uia").start("C:\Program Files (x86)\Pleasant Solutions\KeePass for Pleasant Password Server\KeePass.exe")  # nopep8
app.window(title='Log in to Pleasant Password Server').type_keys("TEST_PASSWORD")
app.window(title='Log in to Pleasant Password Server').child_window(title="Login", auto_id="btnLogin", control_type="Button").click()  # nopep8

time.sleep(2)


# Step 2: Nativate to Obsurv Pub and select
treeView = app.window(title='Pleasant Password Server - KeePass Password Safe').TreeView  # nopep8
treeView.get_item([u'GIS&ICT', 'Obsurv Consultants', 'Obsurv.nl', 'Obsurv Pub']).click_input(double=True)  # nopep8
time.sleep(2)

# Step 3: Get list of all accounts
ListBox = app.window(title='Pleasant Password Server - KeePass Password Safe')['ListBox']  # nopep8
accounts = ListBox.items()


#  Step 4: Loop through each account and reset password and save sql update file
for idx, account in enumerate(accounts):
    if idx >= 2:
        if idx == 105:
            pass
        else:
            account_Name = account.texts()[0]
            account.select()
            keyboard.send_keys('{ENTER}')
            time.sleep(0.5)
            keyboard.send_keys('{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{ENTER}')
            time.sleep(0.5)
            keyboard.send_keys('{DOWN}{ENTER}')
            time.sleep(0.5)
            keyboard.send_keys('{TAB}{TAB}{TAB}{DOWN}{DOWN}{DOWN}{DOWN}{DOWN}')
            time.sleep(0.5)
            keyboard.send_keys('{TAB}{TAB}{TAB}{ENTER}')
            time.sleep(0.5)
            keyboard.send_keys('{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{ENTER}')
            time.sleep(1)

            
            account.click_input(button="right")
            keyboard.send_keys('{DOWN}{DOWN}{ENTER}')
            time.sleep(0.5)
            new_password = clipboard.GetData(1).decode('utf-8')

            sql = f'''set define off
define hash_password="{new_password}"
set define on


declare
l_passwordhash VARCHAR2(128 CHAR) := q'#&hash_password#';
begin
    select alg_autorisatie_pck.passwordhash(upper('helpdesk@sweco.nl'),l_passwordhash) into l_passwordhash from dual;
    update alg_gebruikers gbr set gbr.password = l_passwordhash where gbr.e_mailadres = upper('helpdesk@sweco.nl');
    commit;
end;
/
exit;
'''
            text_file = open(f"{OUTPUT}/{account_Name}.sql", "w")
            n = text_file.write(sql)
            text_file.close()
            print(idx, account, account_Name)
            account.select()
            keyboard.send_keys('{DOWN}')
            time.sleep(1)
            

    

# ListBox.items()[2].click_input(button="right")



# ListBox.items()[2].click_input(button="right")
# keyboard.send_keys('{DOWN}{DOWN}{DOWN}{DOWN}{DOWN}{DOWN}{ENTER}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{ENTER}{DOWN}{ENTER}{ENTER}{TAB}{TAB}{TAB}{TAB}{TAB}{TAB}{ENTER}')
# time.sleep(1)

# ListBox.items()[2].click_input(button="right")
# keyboard.send_keys('{DOWN}{DOWN}{DOWN}{DOWN}{DOWN}{DOWN}{ENTER}')
