from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from time import sleep
import os # Modulo para dar comandos ao CMD
from datetime import date
from time import strftime # Modulo para saber o horario do PC
from telasleeptime import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow

##################################################################
#                                                                #
#          DESENVOLVIDO POR @SAMIRMACIEL                         #
#          QT DESGINER                                           #
#          PYQT5  ****                                           #
#                                                                #
##################################################################

class TelaSleep(QMainWindow):
    sistema_hora  = 0
    sistema_minuto = 0
    def __init__(self, parent=None):
        super(TelaSleep, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.sleep_ligado = self.Calculo_hora(verificaestado=True) # ==> VARIAVEL DE CONTROLE PARA SABER SE JÁ ESTÁ OU NÃO ATIVADO O SLEEP.
        self.ui.btnSair.clicked.connect(lambda: self.close())
        self.ui.btnComecar.clicked.connect(self.Setando_tempo)
        self.ui.btnResetar.clicked.connect(self.Cancelando)
    
    def Setando_tempo(self):
        self.tempo = self.ui.timeEdit.time().toString().split(':')
        self.hora = int(self.tempo[0])
        self.minuto = int(self.tempo[1])
        ######################################################################################### VERIFICA SE A HORA OU O MINUTO SETADOS PELO USUÁRIO, SÃO DIFERENTES DE 0. SE FOR
        if self.hora or self.minuto != 0:                                                       # VERDADEIRO, FAZ OUTRA VERIFICAÇÃO. SE O SLEEP NÃO ESTIVER JÁ FUNCIONANDO, ENTÃO
            if not self.sleep_ligado:                                                           # CHAMA A FUNÇÃO 'DESLIGA' COM OS PARAMENTROS DE HORA E MINUTO SETADOS PELO USUÁRIO,
                self.Desliga(self.hora,self.minuto)                                             # E A FUNÇÃO 'DESLIGA', ENVIA O COMANDO PARA O CMD COM A HORA E DATA CONVERTIDOS PARA
                self.ui.lblTempoSetado.setText(self.Calculo_hora(self.hora, self.minuto))       # SEGUNCOS. APÓS SETA O TEXTO DO 'LBLTEMPOSETADO' CHAMANDO A FUNÇÃO 'CALCULO_HORA',
                arquivo = open('registro.txt', 'wt')                                            # QUE RETORNA O HORARIO LOCAL QUE VAI SER DESLIGADO O PC. SEGUINDO, ESCREVE NO ARQUIVO
                arquivo.write(f'{self.hora_set};{self.minuto_set};{self.dia}')                             # 'REGISTRO.TXT' A HORA E O MINUTO SETADO PELO USUÁRIO. POR FIM DEIXA COMO VERDADEIRO,
                arquivo.close()
                self.ui.label_3.setText('DESLIGA AS: ')                                                                 # A VARIAVEL DE CONTROLE 'SLEEP_LIGADO'.
                self.sleep_ligado = True
            else:
                self.ui.label_5.setText('AGENDAMENTO DE DESLIGAMENTO ATIVO')
                                                                     #
        #########################################################################################

    def Cancelando(self): ########################### ESTÁ FUNÇÃO TEM COMO FUNCIONALIDADE CANCELAR O DESLIGAMENTO DO PC, INICIA SETANDO O 'LBLTEMPOSETADO' PRA VAZIO. DEPOIS MUDA
        self.ui.lblTempoSetado.setText('')          # A VARIAVEL DE CONTROLE 'SLEEP_LIGADO' PRA FALSO, ENTÃO É A ABERTO O ARQUIVO 'REGISTRO.TXT' E GRAVADO O HORARIO 0:0, OU SEJA 
        self.sleep_ligado = False                   # NÃO EXISTE MAIS UM HORARIO SETADO. POR FIM ELA RETORNA O COMANDO PARA O CMD CANCELAR O DESLIGAMENTO.     
        arquivo = open('registro.txt', 'wt')        #
        arquivo.write(f'{30};{100};{0}')            #
        arquivo.close()                             #
        self.ui.label_3.setText('')                 #
        self.ui.label_5.setText('')                 #
        return os.system('shutdown -a')
                                                    #
                          ###########################

    ############################################################### ESTÁ FUNÇÃO CONTEM ALGUNS PARAMENTROS, PARA FAZER COISAS E RETORNAR RESULTADOS ESPECIFICOS. 'verificaestado' VERIFICA
    def Calculo_hora(self, h=0, m=0, verificaestado=False): # SE O HORARIO REGISTRADO NO ARQUIVO 'REGISTRO.TXT' AINDA ESTÁ VALIDO COMPARANDO-O COM O HORARIO DO SISTEMA, CASO
        hora_usuario = h                                          # AINDA ESTEJA, ELE SETA O 'LBLTEMPOSETADO' PARA O HORARIO DO 'REGISTRO.TXT'. 'CHECK2' FAZ A MESMA FUNÇÃO DA 'verificaestado'
        minuto_usuario = m                                        # POREM RETORNA UM BOOLEAN.
        self.hora_check = 0                                       #
        self.minuto_check = 0                                     #
        self.sitema_hora = int(strftime('%H'))                    # ==> DEFININDO UMA VARIAVEL COM A HORA DO SISTEMA
        self.sistema_minuto = int(strftime('%M'))                 # ==> DEFININDO UMVA VARIAVEL COM O MINUTO DO SISTEMA
        self.hora_set = hora_usuario + self.sitema_hora           # ==> SOMANDO A HORA DO SISTEMA COM A HORA SETADA PELO USUÁRIO (QUE É DEFINIDO PELO PARAMETRO 'H' DA FUNÇÃO)
        self.minuto_set = minuto_usuario + self.sistema_minuto    # ==> SOMANDO O MINUTO DO SISTEMA COM O MINUTO SETADO PELO USUÁRIO (QUE É DEFINIDO PELO PARAMETRO 'M' DA FUNÇÃO)
        self.dia = date.today().day                               # ==> SETANDO VARIAVEL DIA COM O DIA DO SISTEMA
        if self.minuto_set > 59:                                  #==
            self.minuto_set -= 59                                 #  | 
            self.hora_set += 1                                    #  |
        if self.hora_set >= 24:
            self.dia += 1                                    #  | CONDIÇÕES QUE FAZEM O CALCULO PARA DEFINIR EM QUE HORA E MINUTO DO SISTEMA O COMPUTADOS VAI SER DESLIGADO.
            self.hora_set -= 24                                   #  |
    ###############################################################==                                        
        if verificaestado:
            arquivo = open('registro.txt', 'rt')
            for linha in arquivo:
                dados = linha.split(';')
                self.hora_check = int(dados[0])
                self.minuto_check = int(dados[1])
                self.dia_check = int(dados[2])
            arquivo.close()
            if  self.dia <= self.dia_check:
                if  self.sitema_hora <= self.hora_check or self.dia < self.dia_check:
                    if self.sistema_hora < self.hora_check or self.dia < self.dia_check:
                        self.ui.lblTempoSetado.setText(f'{self.hora_check}:{self.minuto_check}')
                        self.ui.label_3.setText('DESLIGA AS:')
                        return True
                    if self.sitema_hora == self.hora_check and self.sistema_minuto < self.minuto_check:
                        self.ui.lblTempoSetado.setText(f'{self.hora_check}:{self.minuto_check}')
                        self.ui.label_3.setText('DESLIGA AS: ')
                        return True
                else:
                    return False
            else:
                return False
        if self.minuto_set < 10:
            self.minuto_set = f'0{self.minuto_set}'
        return f'{self.hora_set}:{self.minuto_set}'
           
        
    ################################################# FUNÇÃO CHAMADA PRA CONVERTER AS HORAS E MINUTOS EM SEGUNDOS, E ASSIM ENVIAR PARA O CMD O COMANDO PARA AGENDAR O DESLIGAMENTO.
    def Desliga(self, hora, minuto):                #
        minutos = minuto * 60                       # ==> CALCULA OS MINUTOS EM SEGUNDOS.
        horas = hora * 3600                         # ==> CALCULA AS HORAS EM SEGUNDOS.
        tempo = minutos + horas                     # ==> FAZ A SOMA DAS HORAS E MINUTOS EM SEGUNDOS.
        cmd = os.system(f'shutdown -s -t {tempo}')  # ==> ATRAVÉS DO MODULO 'OS' INSTANCIA UMA VARIAVEL COM O COMANDO PARA O AGENDAMENTO DO DESLIGAMENTO DO PC.
        return cmd                                  # ==> RETORNA O COMANDO PARA O CMD.
    #################################################
            



        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    home = TelaSleep()
    home.show()
    sys.exit(app.exec_())