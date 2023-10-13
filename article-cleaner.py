#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 20:20:35 2023

@author: labuer
"""
import argparse
import re
import os
import sys

def clean_text(text):
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'© MST 2023  - Todos os direitos reservados', '', text, flags=re.DOTALL)
    text = re.sub(r'Quem Somos', '', text, flags=re.DOTALL)

    
    text = re.sub(r'Leia também\:.*', '', text)
    text = re.sub(r'Salve meu nome\, e-mail.*', '', text, flags=re.DOTALL)
    text = re.sub(r'Jornal A Verdade. Todo o conteúdo pode ser livremente reproduzido.*', '', text, flags=re.DOTALL)

    
    text = re.sub(r'Ouça a entrevista na íntegra no tocador de áudio abaixo do título desta matéria\..*', '', text)
    text = re.sub(r'Edição\:.*', '', text, flags=re.DOTALL)
    text = re.sub(r'Clique aqui.*', '', text, flags=re.DOTALL)
    text = re.sub(r'Confira abaixo a entrevista.*', '', text, flags=re.DOTALL)
    text = re.sub(r'Fonte\:.*', '', text, flags=re.DOTALL)
    text = re.sub(r'Assista\:.*', '', text, flags=re.DOTALL)

    text = re.sub(r'Copyright.*', '', text)
    text = re.sub(r'Leia também\:.*', '', text)
    text = re.sub(r'Salve meu nome\, e-mail.*', '', text, flags=re.DOTALL)
    text = re.sub(r'Jornal A Verdade. Todo o conteúdo pode ser livremente reproduzido.*', '', text, flags=re.DOTALL)

    text = re.sub(r'Você que chegou até aqui e que acredita em uma mídia autônoma.*', '', text, flags=re.DOTALL)
    # Replace multiple occurrences of any punctuation mark with a single instance
    text = re.sub(r'([!@#$%^&*()_+={}\[\]:;"\'<>,.?/~`|\\-])\1+', r'\1', text)
    text = re.sub(r'\(\*\).*', '', text, flags=re.DOTALL)
    text = re.sub(r'Redação ICL Economia', '', text)
    text = re.sub(r'Com informações das agências Somos um instituto de educação e cultura que luta para libertar as pessoas pelo conhecimento através de conteúdos primordiais para o desenvolvimento humano, de forma simplificada e acessível. Saiba Mais', '', text, flags=re.DOTALL)
    
    

    return text


def generate_unique_filename(output_dir, filename, extension):
    counter = 1
    unique_name = os.path.join(output_dir, f"{filename}_{counter}{extension}")
    while os.path.exists(unique_name):
        counter += 1
        unique_name = os.path.join(output_dir, f"{filename}_{counter}{extension}")
    return unique_name

def main():
    parser = argparse.ArgumentParser(description='Clean text files using provided rules.')
    parser.add_argument('--root_dir', type=str, default='./', help='Root directory to start searching for txt files')
    parser.add_argument('--output_dir', type=str, default='./cleaned_files', help='Directory to save cleaned txt files')
    
    args = parser.parse_args()
    root_dir = args.root_dir
    output_dir = args.output_dir

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if not filename.endswith('.txt'):
                continue
            
            file_path = os.path.join(dirpath, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                original_text = f.read()

            cleaned_text = clean_text(original_text)
            
            base_name, extension = os.path.splitext(filename)
            output_file_path = os.path.join(output_dir, f"{base_name}_cleaned{extension}")

            if os.path.exists(output_file_path):
                output_file_path = generate_unique_filename(output_dir, base_name, extension)
            
            with open(output_file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)

            print(f"Cleaned {file_path} and saved as {output_file_path}.")

if __name__ == '__main__':
    main()