from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys, time
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="prismon7k7", database="conversordb", auth_plugin="mysql_native_password")
cursor = mydb.cursor()

class Interface:
    def __init__(self, master=None):
        def registrar_conta():
            
            if self.reguser.get() != '' and self.regemail.get() != '' and self.regsenha.get() != '' and self.regsenha.get() == self.regconfsenha.get():
                registro_usuario = self.reguser.get()
                registro_email = self.regemail.get()
                registro_senha = self.regsenha.get()
                registro_confirmarsenha = self.regconfsenha.get()

                query = "SELECT nome, email FROM usuario WHERE nome = %s OR email = %s;"
                cursor.execute(query, (registro_usuario, registro_email))
                conta_igual = str(cursor.fetchall())
                
                if conta_igual == '[]':
                    query = "INSERT INTO usuario(nome, email, senha, dataCriacao) VALUES(%s, %s, %s, NOW())"
                    cursor.execute(query, (registro_usuario, registro_email, registro_senha))
                    mydb.commit()

                    self.textreglog.config(text="Conta registrada com sucesso!")
                else:
                    self.textreglog.config(text="Essa conta já existe!")
            
            elif self.reguser.get() == '' or self.regemail.get() == '' or self.regsenha.get() == '':
                self.textreglog.config(text="Preencha todos os campos!")
            elif self.regsenha.get() != self.regconfsenha.get():
                self.textreglog.config(text="Os campos de senha devem estar iguais!")
            else:
                self.textreglog.config(text="Houve algum erro durante o registro.")

        def mudar_senha():
            senha_antiga = self.senhaAntiga.get()
            nova_senha = self.novaSenha.get()
            usuario = self.login.get()
            senha = self.senha.get()

            if senha == senha_antiga and nova_senha != '' and senha_antiga != '':
                query = "UPDATE usuario SET senha = %s WHERE nome = %s"
                cursor.execute(query, (nova_senha, usuario))
                mydb.commit()
                self.textpasslog.config(text="Requisição completa!")
            elif senha != senha_antiga:
                self.textpasslog.config(text="Senha antiga incorreta!")
            else:
                self.textpasslog.config(text="Preencha corretamente!")

        def add_conversao():
            valor_obtido = self.entrada.get()
            conversao_de = self.convde.get()
            conversao_para = self.convpara.get()
            resultado_conversao = self.widget5.get()
            query = "SELECT MAX(numConv) FROM info_conversao WHERE id_Usuario = "+self.conta_id
            cursor.execute(query)
            lista_numid = cursor.fetchall()
            numConv = str(lista_numid[0])
            numConv = numConv.replace('(', '')
            numConv = numConv.replace(',)', '')
            if numConv == 'None':
                numConv = 0
            numConv = int(numConv) + 1
            descricao_conversao = self.widget_descricao.get()

            query = "INSERT INTO info_conversao(idConv, numConv, id_Usuario, descricao, valorObtido, convDe, convPara, resultado, dataConv) VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, NOW())"
            cursor.execute(query, (numConv, self.conta_id, descricao_conversao, valor_obtido, conversao_de, conversao_para, resultado_conversao))
            mydb.commit()
            limpar_resultados()

        def editar_conversao():
            id_conversao = self.caixa_id.get()
            descricao_conversao = self.caixa_desc.get()

            if messagebox.askyesno("Confirmar edição", "Você deseja mesmo alterar essa descrição?"):
                query = "UPDATE info_conversao SET descricao = '"+descricao_conversao+"' WHERE id_Usuario = "+self.conta_id+" AND numConv = "+id_conversao
                cursor.execute(query)
                mydb.commit()
                limpar_resultados()
            else:
                return True
        
        def excluir_conversao():
            id_conversao = textoid.get()
            if messagebox.askyesno("Confirmar ação de excluir", "Você deseja mesmo excluir os dados dessa conversão?"):
                query = "DELETE FROM info_conversao WHERE id_Usuario = "+self.conta_id+" AND numConv = "+id_conversao
                cursor.execute(query)
                mydb.commit()
                limpar_resultados()
            else:
                return True

        def pesquisar_resultados():
            q2 = q.get()

            query = "SELECT numConv, descricao, valorObtido, convDe, convPara, resultado, dataConv FROM info_conversao WHERE descricao LIKE '%"+q2+"%' and id_Usuario = "+self.conta_id
            cursor.execute(query)
            rows = cursor.fetchall()
            atualizar_tabela(rows)

        def limpar_resultados():
            query = "SELECT numConv, descricao, valorObtido, convDe, convPara, resultado, dataConv from info_conversao WHERE id_Usuario = "+self.conta_id
            cursor.execute(query)
            rows = cursor.fetchall()
            atualizar_tabela(rows)
        
        def agrupar_tipoconversao():
            query = "SELECT numConv, descricao, valorObtido, convDe, convPara, resultado, dataConv from info_conversao WHERE id_Usuario = "+self.conta_id+" ORDER BY convDe ASC"
            cursor.execute(query)
            rows = cursor.fetchall()
            atualizar_tabela(rows)
        
        def agrupar_tipodata():
            query = "SELECT numConv, descricao, valorObtido, convDe, convPara, MAX(resultado), dataConv FROM info_conversao WHERE id_Usuario = "+self.conta_id+" GROUP BY dataConv"
            cursor.execute(query)
            rows = cursor.fetchall()
            atualizar_tabela(rows) 

        def agrupar_tipoid():
            query = "SELECT numConv, descricao, valorObtido, convDe, convPara, resultado, dataConv from info_conversao WHERE id_Usuario = "+self.conta_id+" GROUP BY numConv"
            cursor.execute(query)
            rows = cursor.fetchall()
            atualizar_tabela(rows)

        def atualizar_tabela(rows):
            table_base.delete(*table_base.get_children())
            for i in rows:
                table_base.insert('', 'end', values=i)

        def abrir_Consulta():
            consbg.place(x=0, y= 0)

            consbgline.place(x=0, y=0)

            self.cabecalho.place(x=20, y=5)

            table_base.place(x=13, y=30)

            query = "SELECT numConv, descricao, valorObtido, convDe, convPara, resultado, dataConv from info_conversao WHERE id_Usuario = "+self.conta_id
            cursor.execute(query)
            rows = cursor.fetchall()
            atualizar_tabela(rows)

            self.voltar3.place(x=540, y=265)
            
            self.texto_pesquisa.place(x=20, y=210)
            self.entrada_pesquisa.place(x=20, y=230)
            self.botao_pesquisa.place(x=20, y=255)
            self.botao_limpar.place(x=95, y=255)

            self.tid.place(x=240, y=190)
            self.tdesc.place(x=240, y=210)

            self.caixa_id.place(x=265, y=190)
            self.caixa_desc.place(x=240, y=230)

            self.botao_att.place(x=240, y=260)
            
            self.botao_excluir.place(x=290, y=260)

            textagrupar.place(x=425, y=185)
            gopt1.place(x=425, y=205)
            gopt2.place(x=425, y=225)
            gopt3.place(x=425, y=245)
            
        def fechar_Consulta():
            consbg.place_forget()

            consbgline.place_forget()

            self.cabecalho.place_forget()

            table_base.place_forget()

            self.voltar3.place_forget()
            
            self.texto_pesquisa.place_forget()
            self.entrada_pesquisa.place_forget()
            self.botao_pesquisa.place_forget()
            self.botao_limpar.place_forget()
            
            self.tid.place_forget()
            self.tdesc.place_forget()

            self.caixa_id.place_forget()
            self.caixa_desc.place_forget()

            self.botao_att.place_forget()
            
            self.botao_excluir.place_forget()

            textagrupar.place_forget()
            gopt1.place_forget()
            gopt2.place_forget()
            gopt3.place_forget()

        def fechar_Config():
            settbg.place_forget()
            settleftbg.place_forget()

            self.info_conta.place_forget()

            self.info_user.place_forget()

            self.info_email.place_forget()

            self.info_criacaoconta.place_forget()

            self.info_NovaSenha.place_forget()

            self.text_senhaAntiga.place_forget()
            self.senhaAntiga.place_forget()

            self.text_novaSenha.place_forget()
            self.novaSenha.place_forget()

            self.botaoMudarSenha.place_forget()

            self.textpasslog.place_forget()
            self.textpasslog.config(text="")

            self.voltar2.place_forget()

        def abrir_Config():
            settbg.place(x=0, y=0)
            settleftbg.place(x=0, y=0)

            self.info_conta.place(x=10, y=10)

            self.info_user.place(x=10, y=40)

            self.info_email.place(x=10, y=60)

            self.info_criacaoconta.place(x=10, y=80)

            self.info_NovaSenha.place(x=250, y=10)

            self.text_senhaAntiga.place(x=330, y=70)
            self.senhaAntiga.place(x=330, y=90)

            self.text_novaSenha.place(x=330, y=120)
            self.novaSenha.place(x=330, y=140)

            self.botaoMudarSenha.place(x=370, y=180)

            self.textpasslog.place(x=350, y=210)

            self.voltar2.place(x=10, y=265)
        
        def fechar_Registro():
            regbg.place_forget()
            self.textoreguser.place_forget()

            self.textusuario.place_forget()
            self.reguser.place_forget()

            self.textemail.place_forget()
            self.regemail.place_forget()

            self.textsenha.place_forget()
            self.regsenha.place_forget()

            self.textconfirmsenha.place_forget()
            self.regconfsenha.place_forget()

            self.registrar.place_forget()
            self.voltar.place_forget()

            self.textreglog.place_forget()

        def abrir_Registro():
            regbg.place(x=0, y=0)

            self.textoreguser.place(x=10, y=10)

            self.textusuario.place(x=10, y=50)
            self.reguser.place(x=10, y=70)

            self.textemail.place(x=10, y=90)
            self.regemail.place(x=10, y=110)

            self.textsenha.place(x=10, y=130)
            self.regsenha.place(x=10, y=150)

            self.textconfirmsenha.place(x=10, y=170)
            self.regconfsenha.place(x=10, y=190)

            self.registrar.place(x=5, y=220)
            self.voltar.place(x=145, y=220)

            self.textreglog.place(x=10, y=250)            

        def selecionar():
            mark = "-- Seja bem-vindo ao Programa de Conversão para Dados Astronômicos!!"
            self.textlog.config(text=mark)

        # Aparência em Canvas

        leftbg = Canvas(None, width=140, height=300)
        leftbg.create_rectangle(0, 0, 140, 300, outline='#6c99e7', fill='#b7cdeb')
        leftbg.place(x=0, y=0)
        biggestbg = Canvas(None, width=540, height=300)
        biggestbg.create_rectangle(0, 0, 540, 300, fill='#ffffff')
        biggestbg.place(x=141, y=0)

        # Esfera de fundo

        esfera = Canvas(None, width=200, height=200)
        esfera.create_oval(200, 200, 0, 0, fill='#ced1d0', width=0)
        esfera.place(x=450, y=200)
        esfera.configure(background='#ffffff', highlightthickness=0)

        # Processo de login

        def login_Show():
            loginbg.place(x=0, y=0)

            self.textologin.place(x=265, y=80)
            self.login.place(x=200, y=100)
            self.textosenha.place(x=270, y=140)
            self.senha.place(x=200, y=160)
            self.entrar.place(x=240, y=190)
            self.botaoReg.place(x=240, y=220)

            self.textloginlog.place(x=210, y=250)

        def login():
            nome_login = self.login.get()
            senha_login = self.senha.get()

            query = "SELECT nome, email, senha, dataCriacao FROM usuario WHERE nome = %s AND senha = %s"
            cursor.execute(query, (nome_login, senha_login))
            verificar_conta = str(cursor.fetchall())

            if verificar_conta != '[]':
                for char in "'":
                    verificar_conta = verificar_conta.replace(char, '')
                for char in "(":
                    verificar_conta = verificar_conta.replace(char, '')
                for char in ")":
                    verificar_conta = verificar_conta.replace(char, '')
                verificar_conta = verificar_conta.replace('datetime.date', '')
                dados_conta = verificar_conta.strip('][').split(', ')
                self.info_user.config(text='Nome:'+dados_conta[0])
                self.info_email.config(text='Email:'+dados_conta[1])
                self.info_criacaoconta.config(text='Conta criada em:'+dados_conta[5]+'-'+dados_conta[4]+'-'+dados_conta[3])

                query = "SELECT idusuario FROM usuario WHERE nome = %s AND senha = %s"
                cursor.execute(query, (nome_login, senha_login))
                lista_id = cursor.fetchall()
                self.conta_id = str(lista_id[0])
                self.conta_id = self.conta_id.replace('(', '')
                self.conta_id = self.conta_id.replace(',)', '')
            
                mark = "Login realizado com sucesso!"
                self.textlog.config(text=mark)

                loginbg.place_forget()

                self.textologin.place_forget()
                self.login.place_forget()
                self.textosenha.place_forget()
                self.senha.place_forget()
                self.entrar.place_forget()
                self.botaoReg.place_forget()
                self.textloginlog.place_forget()
            else:
                self.textloginlog.config(text="Login ou Senha incorretos!")

            
        # Valores essenciais da conversão

        self.convde = StringVar()
        self.convpara = StringVar()

        self.text_entrada = Label(text="Insira o Valor:", font=("Arial", 10, 'bold'), background='#ffffff')
        self.text_entrada.place(x=160, y=20)
        self.entrada = Entry(bd=1)
        self.entrada.place(x=260, y=20)

        # Consultar Página de Ajuda

        def ajuda():
            messagebox.showinfo(title="Instruções e Créditos", message="""Esse programa tem a finalidade de realizar conversões de unidades a partir de uma grandeza física.
Para utilizar, basta seguir os passos:
    - Insira um valor a ser convertido
    - Selecione os tipos de conversão (Converter de - Para)
    - Escreva um detalhe na caixa "Descrição".
    - Aperte o botão de Converter.

Após realizada a conversão, o usuário pode consultar a tabela na opção "Ver Conversões".
            
Feito para a disciplina Banco de Dados, pelo grupo:
    - Lucas Freire
    - Alyne Alves
    - Douglas Levi
    - Thiago Monteiro""")

        # Trocar grandezas

        def temperatura():
            self.convde = StringVar()
            self.convpara = StringVar()

            opt1.config(text="Celsius (C)", variable=self.convde, value="c")
            opt2.config(text="Fahrenheit (F)", variable=self.convde, value="f")
            opt3.config(text="Kelvin (K)", variable=self.convde, value="k")

            opt4.config(text="Celsius (C)", variable=self.convpara, value="c")
            opt5.config(text="Fahrenheit (F)", variable=self.convpara, value="f")
            opt6.config(text="Kelvin (K)", variable=self.convpara, value="k")

        # Calcular a conversão
        def converter():
            calculo = 0
            if self.entrada.get() != '' and self.convde.get() != '' and self.convpara.get() != '':
                try: # Encontrar o tipo de conversão que escolheu
                    if self.convde.get() == "c" and self.convpara.get() == "f":
                        calculo = (float(self.entrada.get()) * 1.8) + 32
                    elif self.convde.get() == "c" and self.convpara.get() == "k":
                        calculo = float(self.entrada.get()) + 273.15
                    
                    elif self.convde.get() == "f" and self.convpara.get() == "c":
                        calculo = float(self.entrada.get()) / 1.8
                        calculo = calculo - 32
                    elif self.convde.get() == "f" and self.convpara.get() == "k":
                        calculo = ((float(self.entrada.get()) - 32) * (5/9)) + 273.15
                    
                    elif self.convde.get() == "k" and self.convpara.get() == "c":
                        calculo = float(self.entrada.get()) - 273.15
                    elif self.convde.get() == "k" and self.convpara.get() == "f":
                        calculo = (float(self.entrada.get()) * (9/5)) - 459.67

                    elif self.convde.get() == self.convpara.get():
                        calculo = float(self.entrada.get())
                    
                    else: # Se não achou as medidas
                        print("Erro ao detectar medidas")
                except IndexError: # Se houve erro de indexação
                    calculo = 0

                try:
                    calculo = float(calculo)
                except:
                    calculo = "Apenas números/ponto(decimal)!"
                
                try:
                    if (float(calculo) < 0):
                        calculo = calculo*(-1)
                except ValueError:
                    calculo = "Preencha corretamente!"


            else:
                calculo = "Informações faltando!"

            resultado = calculo
            self.widget5.delete(0, "end")
            self.widget5.insert(0, str(resultado))

            if type(calculo) == float:
                add_conversao()

        # Menu de escolher grandezas abaixo

        self.container1 = Frame(master)
        self.container1.grid(row=0, column=1, padx=8, pady=4)
        self.container1.configure(background='#b7cdeb')

        self.msg1 = Label(self.container1, text="Escolher Grandeza:", font=("Arial", 10, 'bold'))
        self.msg1.grid(row=1, column=1)
        self.msg1.configure(background='#b7cdeb')

        self.container2 = Frame(master)

        self.textlog = Label(None, text="")
        self.textlog.place(x=141, y=280)

        def enter(e):
            self.grandeza1.configure(background='#0b338e')
        
        def leave(e):
            self.grandeza1.configure(background='#1c65ef')

        self.grandeza1 = Button(self.container1, text="Temperatura", font=("Arial", 10, 'bold'), command=temperatura)
        self.grandeza1.grid(row=2, column=1, pady=5)
        self.grandeza1.configure(background='#1c65ef', highlightcolor='#1c65ef', highlightthickness=5, borderwidth=0)

        self.grandeza1.bind("<Enter>", enter)
        self.grandeza1.bind("<Leave>", leave)

        #=Linha separadora feita através de canvas=

        canvas2 = Canvas(None, width=2, height=80)
        canvas2.create_line(3, 0, 3, 80, fill='gray')
        canvas2.place(x=345, y=50)
        #===========================================

        # Opções de conversão

        textde = Label(None, text="Converter de:", font=("Arial", 10, 'bold'), background='#ffffff').place(x=160, y=50)

        opt1 = Radiobutton(None, text="Celsius (C)", font=("Arial", 10, 'bold'), background='#ffffff', variable=self.convde, value="c", command=selecionar)
        opt1.place(x=160, y=70)
        opt2 = Radiobutton(None, text="Fahrenheit (F)", font=("Arial", 10, 'bold'), background='#ffffff', variable=self.convde, value="f", command=selecionar)
        opt2.place(x=160, y=90)
        opt3 = Radiobutton(None, text="Kelvin (K)", font=("Arial", 10, 'bold'), background='#ffffff', variable=self.convde, value="k", command=selecionar)
        opt3.place(x=160, y=110)

        textpara = Label(None, text="Para:", font=("Arial", 10, 'bold'), background='#ffffff').place(x=350, y=50)

        opt4 = Radiobutton(None, text="Celsius (C)", font=("Arial", 10, 'bold'), background='#ffffff', variable=self.convpara, value="c", command=selecionar)
        opt4.place(x=350, y=70)
        opt5 = Radiobutton(None, text="Fahrenheit (F)", font=("Arial", 10, 'bold'), background='#ffffff', variable=self.convpara, value="f", command=selecionar)
        opt5.place(x=350, y=90)
        opt6 = Radiobutton(None, text="Kelvin (K)", font=("Arial", 10, 'bold'), background='#ffffff', variable=self.convpara, value="k", command=selecionar)
        opt6.place(x=350, y=110)

        self.widget_descricao = Entry(bd=1)
        self.widget_descricao.insert(END, 'Descrição')
        self.widget_descricao.place(x = 350, y = 150)

        #===========================================

        def enter3(e):
            self.widget2.configure(background='#c93c3d')
        
        def leave3(e):
            self.widget2.configure(background='#7a7a7a')

        self.widget2 = Button(None, text="   Sair   ", font=("Arial", 10, 'bold'), command=login_Show)
        self.widget2.place(x = 535, y = 270)
        self.widget2.configure(background='#7a7a7a', highlightcolor='#1c65ef', highlightthickness=5, borderwidth=0)

        self.widget2.bind("<Enter>", enter3)
        self.widget2.bind("<Leave>", leave3)

        def enter2(e):
            self.widget3.configure(background='#0b338e')
        
        def leave2(e):
            self.widget3.configure(background='#1c65ef')

        self.widget3 = Button(root, text="      Ajuda      ", font=("Arial", 10, 'bold'), command=ajuda)
        self.widget3.place(x = 20, y = 270)
        self.widget3.configure(background='#1c65ef', highlightcolor='#1c65ef', highlightthickness=5, borderwidth=0)

        self.widget3.bind("<Enter>", enter2)
        self.widget3.bind("<Leave>", leave2)

        def enter4(e):
            self.settbutton.configure(background='#0b338e')
        def leave4(e):
            self.settbutton.configure(background='#1c65ef')

        self.settbutton = Button(root, text="Configurações", font=("Arial", 10, 'bold'), background='#1c65ef', command=abrir_Config)
        self.settbutton.place(x = 18, y = 230)
        self.settbutton.configure(background='#1c65ef', highlightcolor='#1c65ef', highlightthickness=5, borderwidth=0)


        self.settbutton.bind("<Enter>", enter4)
        self.settbutton.bind("<Leave>", leave4)

        def enter5(e):
            self.searchbutton.configure(background='#0b338e')
        def leave5(e):
            self.searchbutton.configure(background='#1c65ef')

        self.searchbutton = Button(root, text="Ver Conversões", font=("Arial", 10, 'bold'), background='#1c65ef', command=abrir_Consulta)
        self.searchbutton.place(x = 15, y = 190)
        self.searchbutton.configure(background='#1c65ef', highlightcolor='#1c65ef', highlightthickness=5, borderwidth=0)


        self.searchbutton.bind("<Enter>", enter5)
        self.searchbutton.bind("<Leave>", leave5)

        self.widget4 = Button(root, text="Converter!", font=("Arial", 10, 'bold'), command=converter)
        self.widget4.place(x = 180, y = 140)

        self.texto_resultado = Label(root, text="Resultado:", font=("Arial", 10, 'bold'), background='#ffffff').place(x = 165, y = 190)
        self.widget5 = Entry(bd = 1, width=30)
        self.widget5.place(x = 240, y = 190)

        # Tela de login

        loginbg = Canvas(None, width=600, height=300)
        loginbg.create_rectangle(0, 0, 600, 300, fill='#ffffff')
        loginbg.place(x=0, y=0)

        self.textologin = Label(root, text="Usuário:", font=("Arial", 10, 'bold'), background='#ffffff')
        self.textologin.place(x=265, y=80)
        self.login = Entry(bd=1, width=30)
        self.login.place(x=200, y=100)
        self.textosenha = Label(root, text="Senha:", font=("Arial", 10, 'bold'), background='#ffffff')
        self.textosenha.place(x=270, y=140)
        self.senha = Entry(bd=1, width=30)
        self.senha.place(x=200, y=160)
        self.entrar = Button(root, text="Entrar na Conta", font=("Arial", 10, 'bold'), command=login)
        self.entrar.place(x=240, y=190)
        self.botaoReg = Button(root, text="Registrar Conta", font=("Arial", 10, 'bold'), command=abrir_Registro)
        self.botaoReg.place(x=240, y=220)

        self.textloginlog = Label(root, text="", font=("Arial", 10), background='#ffffff')
        self.textloginlog.place(x=210, y=250)

        # Tela de Registro
        
        regbg = Canvas(None, width=600, height=300)
        regbg.create_rectangle(0, 0, 600, 300, fill='#ffffff')
        regbg.place(x=0, y=0)

        self.textoreguser = Label(root, text="Seja bem-vindo, preencha o registro para criar a sua conta.", font=("Arial", 12, 'bold'), background='#ffffff')
        self.textoreguser.place(x=10, y=10)

        self.textusuario = Label(root, text="Usuário:", font=("Arial", 10, 'bold'), background='#ffffff')
        self.textusuario.place(x=10, y=50)
        self.reguser = Entry(bd=1, width=30)
        self.reguser.place(x=10, y=70)

        self.textemail = Label(root, text="Email:", font=("Arial", 10, 'bold'), background='#ffffff')
        self.textemail.place(x=10, y=90)
        self.regemail = Entry(bd=1, width=30)
        self.regemail.place(x=10, y=110)

        self.textsenha = Label(root, text="Senha:", font=("Arial", 10, 'bold'), background='#ffffff')
        self.textsenha.place(x=10, y=130)
        self.regsenha = Entry(bd=1, width=30)
        self.regsenha.place(x=10, y=150)
        self.textconfirmsenha = Label(root, text="Confirmar Senha:", font=("Arial", 10, 'bold'), background='#ffffff')
        self.textconfirmsenha.place(x=10, y=170)
        self.regconfsenha = Entry(bd=1, width=30)
        self.regconfsenha.place(x=10, y=190)

        self.registrar = Button(root, text="Confirmar Registro", font=("Arial", 10, 'bold'), background='#ffffff', command=registrar_conta)
        self.registrar.place(x=5, y=210)
        self.voltar = Button(root, text="Voltar", font=("Arial", 10, 'bold'), background='#ffffff',command=fechar_Registro)
        self.voltar.place(x=145, y=210)

        self.textreglog = Label(root, text="", font=("Arial", 10), background='#ffffff')
        self.textreglog.place(x=10, y=250)

        fechar_Registro()

        # Consultar Conversões

        consbg = Canvas(None, width=600, height=300)
        consbg.create_rectangle(0, 0, 600, 300, fill='#ffffff')
        consbg.place(x=0, y= 0)

        consbgline = Canvas(None, width=8, height=300)
        consbgline.create_rectangle(0, 0, 8, 300, fill='#0b338e', width=0)
        consbgline.place(x=0, y=0)

        self.cabecalho = Label(root, text="Conversões de usuário", font=("Arial", 14, 'bold'), background='#ffffff')
        self.cabecalho.place(x=20, y=5)

        table_base = ttk.Treeview(root, columns=(1, 2, 3, 4, 5, 6, 7), show="headings", height="6")
        table_base.place(x=13, y=30)

        table_base.heading(1, text="N°")
        table_base.column(1, minwidth=0, width=40)
        table_base.heading(2, text="Descrição")
        table_base.column(2, minwidth=0, width=120)
        table_base.heading(3, text="Valor de Entrada")
        table_base.column(3, minwidth=0, width=100)
        table_base.heading(4, text="De")
        table_base.column(4, minwidth=0, width=60)
        table_base.heading(5, text="Para")
        table_base.column(5, minwidth=0, width=60)
        table_base.heading(6, text="Resultado")
        table_base.column(6, minwidth=0, width=100)
        table_base.heading(7, text="Data")
        table_base.column(7, minwidth=0, width=100)

        def pegar_resultado(event):
            rowid = table_base.identify_row(event.y)
            item = table_base.item(table_base.focus())
            textoid.set(item['values'][0])
            textodesc.set(item['values'][1])

        table_base.bind('<Double 1>', pegar_resultado)

        query = "SELECT numConv, descricao, valorObtido, convDe, convPara, resultado, dataConv from info_conversao"
        cursor.execute(query)
        rows = cursor.fetchall()
        atualizar_tabela(rows)

        self.voltar3 = Button(root, text="Voltar", font=("Arial", 10, 'bold'), background='#ffffff', command=fechar_Consulta)
        self.voltar3.place(x=540, y=265)

        q = StringVar()
        self.texto_pesquisa = Label(root, text="Filtrar por descrição:", font=("Arial", 10, 'bold'), background='#ffffff')
        self.texto_pesquisa.place(x=20, y=210)
        self.entrada_pesquisa = Entry(bd=1, textvariable=q)
        self.entrada_pesquisa.place(x=20, y=230)
        self.botao_pesquisa = Button(root, text="Pesquisar", font=("Arial", 10, 'bold'), background='#ffffff', command=pesquisar_resultados)
        self.botao_pesquisa.place(x=20, y=255)
        self.botao_limpar = Button(root, text="Limpar", font=("Arial", 10, 'bold'), background='#ffffff', command=limpar_resultados)
        self.botao_limpar.place(x=95, y=255)

        textoid = StringVar()
        textodesc = StringVar()

        self.tid = Label(root, text="ID:", font=("Arial", 10, 'bold'), background='#ffffff')
        self.tid.place(x=240, y=190)
        self.tdesc = Label(root, text="Descrição:", font=("Arial", 10, 'bold'), background='#ffffff')
        self.tdesc.place(x=240, y=210)

        self.caixa_id = Entry(bd=1, textvariable=textoid)
        self.caixa_id.place(x=265, y=190)
        self.caixa_desc = Entry(bd=1, textvariable=textodesc)
        self.caixa_desc.place(x=240, y=230)

        self.botao_att = Button(root, text="Editar", font=("Arial", 10, 'bold'), background='#ffffff', command=editar_conversao)
        self.botao_att.place(x=240, y=260)
        
        self.botao_excluir = Button(root, text="Excluir", font=("Arial", 10, 'bold'), background='#ffffff', command=excluir_conversao)
        self.botao_excluir.place(x=290, y=260)
        
        textagrupar = Label(None, text="Organizar por:", font=("Arial", 10, 'bold'), background='#ffffff')
        textagrupar.place(x=425, y=185)

        gopt1 = Radiobutton(None, text="ID", font=("Arial", 10, 'bold'), background='#ffffff', command=agrupar_tipoid)
        gopt1.place(x=425, y=205)
        gopt2 = Radiobutton(None, text="Maior Resultado/Data", font=("Arial", 10, 'bold'), background='#ffffff', command=agrupar_tipodata)
        gopt2.place(x=425, y=225)
        gopt3 = Radiobutton(None, text="Conversão", font=("Arial", 10, 'bold'), background='#ffffff', command=agrupar_tipoconversao)
        gopt3.place(x=425, y=245)

        fechar_Consulta()

        # Processo de Mudar Senha

        settbg = Canvas(None, width=600, height=300)
        settbg.create_rectangle(0, 0, 600, 300, fill='#ffffff')
        settbg.place(x=0, y=0)

        settleftbg = Canvas(None, width=240, height=300)
        settleftbg.create_rectangle(0, 0, 240, 300, outline='#6c99e7', fill='#b7cdeb')
        settleftbg.place(x=0, y=0)

        self.info_conta = Label(root, text="Informações do Usuário:", font=("Arial", 11, 'bold'), background='#b7cdeb')
        self.info_conta.place(x=10, y=10)

        self.info_user = Label(root, text="Nome:", font=("Arial", 10, 'bold'), background='#b7cdeb')
        self.info_user.place(x=10, y=40)

        self.info_email = Label(root, text="E-mail:", font=("Arial", 10, 'bold'), background='#b7cdeb')
        self.info_email.place(x=10, y=60)

        self.info_criacaoconta = Label(root, text="Conta criada em:", font=("Arial", 10, 'bold'), background='#b7cdeb')
        self.info_criacaoconta.place(x=10, y=80)

        self.info_NovaSenha = Label(root, text="""     Caso queira mudar de senha, é bem simples!
        Preencha os campos abaixo e confirme.""", font=("Arial", 10, 'bold'), background='#ffffff')
        self.info_NovaSenha.place(x=250, y=10)

        self.text_senhaAntiga = Label(root, text="Senha Antiga:", font=("Arial", 10, 'bold'), background='#ffffff')
        self.text_senhaAntiga.place(x=330, y=70)
        self.senhaAntiga = Entry(bd=1, width=30)
        self.senhaAntiga.place(x=330, y=90)

        self.text_novaSenha = Label(root, text="Nova Senha:", font=("Arial", 10, 'bold'), background='#ffffff')
        self.text_novaSenha.place(x=330, y=120)
        self.novaSenha = Entry(bd=1, width=30)
        self.novaSenha.place(x=330, y=140)

        self.botaoMudarSenha = Button(None, text="Mudar Senha", font=("Arial", 10, 'bold'), background='#ffffff', command=mudar_senha)
        self.botaoMudarSenha.place(x=370, y=180)

        self.textpasslog = Label(root, text="", font=("Arial", 10), background='#ffffff')
        self.textpasslog.place(x=370, y=210)

        def enter3(e):
            self.voltar2.configure(background='#0b338e')
        
        def leave3(e):
            self.voltar2.configure(background='#1c65ef')

        self.voltar2 = Button(None, text="Voltar", font=("Arial", 10, 'bold'), background='#1c65ef', command=fechar_Config)
        self.voltar2.place(x=10, y=265)
        
        self.voltar2.bind("<Enter>", enter3)
        self.voltar2.bind("<Leave>", leave3)
        
        fechar_Config()

# Execução da Aplicação Geral
root = Tk()
root.title("Conversor de Medidas Astronômicas")
root.iconphoto(False, PhotoImage(file='icon.png'))
root.geometry("600x300")
root.resizable(width=False, height=False)
Interface(root)
root.mainloop()