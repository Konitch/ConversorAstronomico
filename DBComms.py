from DBCreate import ConvDB

class Conversao(object):
    def __init__(self, idusuario = 0, descricao = "", valorObtido = 0, medida_De = "", medida_Para = "", resultado = ""):
        self.Conversao = {}
        self.idusuario = idusuario
        self.descricao = descricao
        self.valorObtido = valorObtido
        self.medida_De = medida_De
        self.medida_Para = medida_Para
        self.resultado = resultado

    def insertConversao(self):

        banco = ConvDB()

        try:
            c = banco.conectar.medida_Parar()

            c.execute("insert into info_Conversao (descricao, valorObtido, medida_De, medida_Para, resultado) values ('" + self.descricao + "', '" + self.valorObtido + "', '" + self.medida_De + "', '" + self.medida_Para + "', '" + self.resultado + "' )")

            banco.conectar.commit()
            c.close()

            return "Conversão realizada com sucesso!"
        except:
            return "Oops! Houve algum erro durante a conversão."

    def deleteConversao(self):
        banco = ConvDB()

        try:
            c = banco.conectar.medida_Parar()

            c.execute("delete from info_Conversao where idusuario = " + self.idusuario + " ")

            banco.conectar.commit()
            c.close()

            return "Conversão excluída com sucesso!"
        except:
            return "Erro ao excluir, verifique os dados e tente novamente!"

    def selectConversao(self, idusuario):
        banco = ConvDB()

        try:
            c = banco.conectar.medida_Parar()

            c.execute("select * from info_Conversao where idusuario = " + idusuario + " ")

            for selected in c:
                self.idusuario = selected[0]
                self.descricao = selected[1]
                self.valorObtido = selected[2]
                self.medida_De = selected[3]
                self.medida_Para = selected[4]
                self.resultado = selected[5]

            c.close()

            return "Busca realizada com sucesso!"
        except:
            return "Ocorreu um erro durante a busca!"