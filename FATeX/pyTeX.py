#!/usr/bin/env python3
#
# Автор: Гончаренко Дмитрий, GlowByte Consulting
#
import os, sys, re
import time
from datetime import datetime
from pylatex.utils import italic, NoEscape, bold
from pylatex import Document, Section, Subsection, Command, UnsafeCommand, \
                    Figure, NoEscape, Center, HugeText, SmallText, VerticalSpace, \
                    HorizontalSpace, TextColor, NewLine
from pylatex.base_classes import Environment, CommandBase, Arguments
from pylatex.package import Package
from colorama import init
from termcolor import cprint, colored

#  -------------- Default Arguments -------------- #
args = {'author':'Гончаренко Дмитрий Александрович',
        'what_do':'Что сделано',
        'systems':'SAS RTDM',
        'what_test':'Что тестировано',
        'who_test':'Кем тестировано',
        'role':'Технолог',
        'goal':'Зачем тестировано',
        'test_environment':'SAS RTDM',
        'result':'Приложение работоспособно и работает в соответствие с ожиданиями'}


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Parse cmd and value in line
def get_value(line):
    cmd = ''
    if line.find(':') == -1 or line.find('=') == -1:
        print('Text file parsing', colored('error', 'red'), ': check for :cmd = value')
        sys.exit(0)
    cmd = line[line.find(':')+1:line.find('=')].strip()
    if cmd == 'end':
        return 'end',''
    value = line[line.find('=')+1:].strip()
    if not args.get(cmd):
        print('Command: \'' + cmd + '\'', colored('not found!','red'))
        print(colored('Available cmd:', 'yellow'), args.keys())
        sys.exit(0)
    fio = []
    if cmd == 'author':
        fio = value.split(' ')
        if len(fio) != 3:
            print(fio)
            cprint('Error. Please write full name in \'author\' field!', 'red')
            sys.exit(0)
        args['who_test'] = fio[0] + ' ' + fio[1][0] + '. ' + fio[2][0] + '.'
    return cmd, value


# Parsing txt file 
def parse_text(file):
    print(colored('Parsing file:', 'green'), file, colored('starting!', 'green'))
    with open(file, 'r', encoding='utf-8') as fat:
        value = ''
        cmd = ''
        for line in fat:
            if line.strip() and line.strip()[0] == ':':
                if value and cmd: 
                    rgs[cmd] = value.strip()
                cmd, value = get_value(line.strip())
                if cmd == 'end':
                    break
                continue
            value += line
    cprint('Parsed!', 'red')


# Env class for frame drawing 
class Box(Environment):
    _latex_name = 'textbox'


# Filling TeX document
def fill_document(doc):
    cprint('Generating TeX document!', 'green')
    # Packages
    doc.packages.clear()
    doc.packages.append(Package('cmap'))
    doc.packages.append(Package('inputenc', options='utf8x'))
    doc.packages.append(Package('fontenc', options='T2A'))
    doc.packages.append(Package('babel', options=('russian', 'english')))
    doc.packages.append(Package('hyperref', options='hidelinks'))  
    doc.packages.append(Package('amsthm'))
    doc.packages.append(Package('listings,lstautogobble')) 
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('amsfonts'))
    doc.packages.append(Package('amssymb'))
    doc.packages.append(Package('xcolor,colortbl'))
    doc.packages.append(Package('graphicx'))
    doc.packages.append(Package('subcaption'))
    doc.packages.append(Package('tabularx'))
    doc.packages.append(Package('fullpage'))
    doc.packages.append(Package('fancyhdr'))
    doc.packages.append(Package('tocbibind', options=('nottoc', 'numbib')))
    # Preamble - Dynamic (parsed)
    doc.preamble.append(Command('renewcommand', arguments=(NoEscape(r'\author'), args.get('author'))))
    doc.preamble.append(Command('newcommand', arguments=(NoEscape(r'\whatdo'), args.get('what_do')))) # 1. Что сделано
    doc.preamble.append(Command('newcommand', arguments=(NoEscape(r'\systems'), args.get('systems')))) # 2. Затрагиваемые ИТ системы
    doc.preamble.append(Command('newcommand', arguments=(NoEscape(r'\whattest'), args.get('what_test')))) # 3. Предмет тестирования/FAT
    doc.preamble.append(Command('newcommand', arguments=(NoEscape(r'\whotest'), args.get('who_test')))) # 4. Участники тестирования/FAT
    doc.preamble.append(Command('newcommand', arguments=(NoEscape(r'\role'), args.get('role'))))# 4. Участники тестирования/FAT - Роль
    doc.preamble.append(Command('newcommand', arguments=(NoEscape(r'\goal'), args.get('goal')))) # 5. Цель тестирования/FAT
    doc.preamble.append(Command('newcommand', arguments=(NoEscape(r'\testenvironment'), args.get('test_environment')))) # 6. Среда проведения тестирования/FAT
    doc.preamble.append(Command('newcommand', arguments=(NoEscape(r'\result'), args.get('result')))) # 7. Результат проверки тестирования/FAT
    # Preamble - Static
    doc.preamble.append(Command('pagestyle', 'fancy'))
    doc.preamble.append(Command('renewcommand', arguments=(NoEscape(r'\headrulewidth'), r'0pt')))
    doc.preamble.append(Command('newenvironment', 'textbox', options=(NoEscape(r'1][|X|')), 
                                    extra_arguments=[NoEscape(r'\vspace{1pt}\centering\tabularx{\textwidth}{#1}\hline'),
                                    NoEscape(r'\\\hline\endtabularx\\\vspace{4.5pt}')
                        ]))
    # Document
    img_rsb = resource_path('rsb.png')
    doc.append(Command('selectlanguage', 'russian'))
    doc.append(Command('thispagestyle', 'empty'))
    doc.append(Command('setlength', arguments=(NoEscape(r'\headsep'), NoEscape(r'-2cm'))))
    # Logo
    with doc.create(Figure(position='htp')) as logo:
        logo.add_image(img_rsb, width=NoEscape(r'0.3\textwidth')) 
    # Page Header
    with doc.create(Center()) as centered:
        centered.append(NoEscape(r'\color{blue}{\textbf{\Huge{\underline{FAT}\textbackslash UAT Report}}}'))
    # Starts
    with doc.create(Box()) as env:
        env.append(NoEscape(r'\\ 1. \whatdo \\'))
    doc.append(NoEscape(r'\par\noindent\textbf{2. Затрагиваемые ИТ системы}\par'))
    with doc.create(Box()) as env:
        env.append(NoEscape(r'\systems'))
    doc.append(NoEscape(r'\par\noindent\textbf{3. Предмет тестирования/FAT}\par'))
    with doc.create(Box()) as env:
        env.append(NoEscape(r'\whattest'))
    doc.append(NoEscape(r'\par\noindent\textbf{4. Участники тестирования/FAT}\par'))
    doc.append(NoEscape(r'\begin{textbox}[|X|X|X|]\textbf{Имя}&\textbf{Подразделение}&\textbf{Роль}\\\hline\whotest&ДРР&\role\end{textbox}\par'))
    doc.append(NoEscape(r'\par\noindent\textbf{5. Цель тестирования/FAT}\par'))
    with doc.create(Box()) as env:
        env.append(NoEscape(r'\goal'))
    doc.append(NoEscape(r'\par\noindent\textbf{6. Среда проведения тестирования/FAT}\par'))
    with doc.create(Box()) as env:
        env.append(NoEscape(r'\testenvironment'))
    doc.append(NoEscape(r'\par\noindent\textbf{7. Результат проверки тестирования/FAT}\par'))
    with doc.create(Box()) as env:
        env.append(NoEscape(r'\result'))
    doc.append(NoEscape(r'\par\noindent\textbf{8. Заключение по результату проверки тестирования/FAT}\par'))
    with doc.create(Box()) as env:
        env.append(NoEscape(r'\footnotesize{\emph{В процессе проведения FAT установлено, что функциональность ПО полностью соответствует предъявленным требованиям. Установку доработок в СЕРТ среду считаем возможным.}}'))
    doc.append(NoEscape(r'\par\noindent\textbf{9. Выявленные замечания по результату проверки тестирования/FAT}\par'))
    with doc.create(Box()) as env:
        env.append(NoEscape(r''))
    doc.append(NoEscape(r'\par\noindent\textbf{10. Финальное решение по результату проверки тестирования/FAT}\par'))
    doc.append(NoEscape(r'\begin{textbox}[|l|X|]\textbf{Test\textbackslash FAT статус}&\textbf{Пройдено}\\\hline\textbf{Комментарий}&\\&\end{textbox}\par'))
    doc.append(NoEscape(r'\vspace{-7pt}\par'))
    doc.append(NoEscape(r'\begin{textbox}[|l|X|p{0.2\textwidth}|]Дата&Фамилия, Имя Бизнес представителя&Подпись\\\hline\today&\author &\end{textbox}\par'))
    doc.append(NoEscape(r'\vspace{-1.5cm}'))
    doc.append(NoEscape(r'\hspace{12.5cm}\includegraphics[width=70pt]{sign}'))
    cprint('Generated!', 'red')



# Creating TeX and PDF
def createTeX(file):
    doc = Document(file, documentclass='extarticle', document_options=('12pt', 'a4paper'))
    
    parse_text('fat.txt')
    fill_document(doc)
    
    cprint('Rendering PDF!', 'green')
    doc.generate_pdf(clean_tex=True, compiler='pdflatex')
    doc.generate_tex()
    print(colored('PDF created:', 'red'), file + '.pdf')
    cprint('Cleaning repository!', 'cyan')
    if os.path.exists('FAT.tex'):
        os.remove('FAT.tex')
    cprint('Finished!', 'magenta', attrs=['bold'])


def main():
    cprint('Starting autoFAT. v1.0', 'yellow', attrs=['bold'])

    createTeX('FAT')
    time.sleep(1)

if __name__ == '__main__':
    init()
    if not os.path.exists('sign.png'):
        cprint('ERROR, no signature image: sign.png found!', 'red')
        sys.exit(1)
    if not os.path.exists('fat.txt'):
        cprint('ERROR, no text file: fat.txt found!', 'red')
        sys.exit(1)
    main()
