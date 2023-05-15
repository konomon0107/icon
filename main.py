import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import joblib,configparser
from PIL import Image

inifile = configparser.ConfigParser()
inifile.read('settings.ini','utf-8')

class Application(tk.Frame):
    
    def __init__(self,master=None):
        super().__init__(master)
        self.config(width=600,height=200,bg='#FFDEAD')
        self.pack(expand=1,fill=tk.BOTH)
        self.create_widgets()
    
    def create_widgets(self):
        # pngファイルパス選択ラベル
        self.pnglbl = tk.Label(self,text='pngファイルパス',bg='#FFDEAD',font=('MSゴシック',12,'bold'))
        self.pnglbl.place(x=10,y=10)
        # pngファイルパス入力エントリ
        self.filepath = tk.StringVar()
        self.filepath.set(inifile['PNG']['PNGPATH'])
        self.entry_path = tk.Entry(self,textvariable=self.filepath,width=65,font=('MSゴシック',12))
        self.entry_path.place(x=10,y=40)
        # pngファイル選択ダイアログボタン
        self.pngbtn = tk.Button(self,text='pngファイル選択',width=15,\
                                font=('MSゴシック',10,'bold'),\
                                command=self.pngbtn_clicked)
        self.pngbtn.place(x=450,y=70)
        #icoファイル名ラベル
        self.icolbl = tk.Label(self,text='変換後ファイル名',bg='#FFDEAD',font=('MSゴシック',10,'bold'))
        self.icolbl.place(x=10,y=70)
        #icoファイル変換後のファイル名入力エントリ
        self.iconame = tk.StringVar()
        self.icofilename = tk.Entry(self,textvariable=self.iconame,width=15,font=('MSゴシック',12))
        self.icofilename.place(x=10,y=90)
        # サイズ選択ラジオボタン
        self.radio_value = tk.IntVar(value=64)
        self.radio1 = tk.Radiobutton(self,text='16x16',value=16,\
                                      variable=self.radio_value,\
                                      command=self.radio_clicked,\
                                      bg='#FFDEAD',font=('MSゴシック',14,'bold'))
        self.radio1.place(x=10,y=150)
        self.radio2 = tk.Radiobutton(self,text='32x32',value=32,\
                                      variable=self.radio_value,\
                                      command=self.radio_clicked,\
                                      bg='#FFDEAD',font=('MSゴシック',14,'bold'))
        self.radio2.place(x=110,y=150)
        self.radio3 = tk.Radiobutton(self,text='48x48',value=48,\
                                      variable=self.radio_value,\
                                      command=self.radio_clicked,\
                                      bg='#FFDEAD',font=('MSゴシック',14,'bold'))
        self.radio3.place(x=210,y=150)
        self.radio4 = tk.Radiobutton(self,text='64x64',value=64,\
                                      variable=self.radio_value,\
                                      command=self.radio_clicked,\
                                      bg='#FFDEAD',font=('MSゴシック',14,'bold'))
        self.radio4.place(x=310,y=150)
        # ラジオボタン初期値をiniファイルにセット
        inifile['RADIO']['VALUE'] = '64'
        # iniファイル書込み
        with open("settings.ini", "w", encoding="utf-8") as configfile:
            inifile.write(configfile, True)
        # 変換開始ボタン
        self.startbtn = tk.Button(self,text='変換開始',width=15,\
                                  font=('MSゴシック',10,'bold'),\
                                  command=self.startbtn_clicked)
        self.startbtn.place(x=450,y=150)
    
    def pngbtn_clicked(self):
        file_type = [("PNGファイル","*.png;")]
        dir = inifile['PNG']['PATH']
        fld = filedialog.askopenfilename(filetypes=file_type, initialdir=dir)
        slippath = fld.split('/')[:-1]
        slippath2 = fld.split('/')[-1]
        slippath3 = slippath2.split('.')[0]
        fldpath = ''
        for i in slippath:
            fldpath += i + '/'

        # ファイルが選択されたとき
        if fld != "":
            file_path = [fld]
            joblib.dump(file_path,'csv_file_path.txt',compress=3)
            self.filepath.set(fld)
            self.iconame.set(slippath3+'.ico')
            inifile['PNG']['PNGPATH'] = fld
            inifile['PNG']['PATH'] = fldpath
            # iniファイル書込み
            with open("settings.ini", "w", encoding="utf-8") as configfile:
                inifile.write(configfile, True)
    
    def radio_clicked(self):
        inifile['RADIO']['VALUE'] = str(self.radio_value.get())
        # iniファイル書込み
        with open("settings.ini", "w", encoding="utf-8") as configfile:
            inifile.write(configfile, True)
    
    def startbtn_clicked(self):
        filename = self.filepath.get()
        size = int(inifile['RADIO']['VALUE'])
        icofilename = self.iconame.get()
        if '.ico' in str(icofilename):
          img = Image.open(filename)
          icon_size = [(size,size)]
          img.save('../../'+ icofilename,sizes=icon_size)
          messagebox.showinfo('メッセージ',f'icoファイル:{icofilename} サイズ:{size}x{size}\n作成完了。')
        else:
            messagebox.showwarning('エラーメッセージ','変換後のファイル名は〇〇.icoで指定して下さい。')

def main():
    window = tk.Tk()
    window.geometry('600x200')
    window.title('PNG → ICO 変換ツール')
    # Icon_image Path
    iconfile = '.\\ico_convert.ico'
    # Icon_image Set
    window.iconbitmap(default=iconfile)
    app = Application(master=window)
    app.mainloop()

if __name__ == '__main__':
    main()