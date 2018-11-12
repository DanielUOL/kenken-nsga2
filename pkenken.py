#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import os
from os import path,listdir
import numpy as np
import matplotlib.pyplot as plt
from shapely import geometry, ops

class Cage:
    def __init__(self,n,result,operation,points):
        self.n=n
        self.result=result
        self.operation=operation
        self.points=points
        if operation == '=':
            self.values = [self.result]
        else:
            self.values = [0]*len(points)
                
                
    def __repr__(self):
        return ' '.join(map(str,[self.result,self.operation,self.points,self.values]))

    
    def op_str(self):
        if self.operation == '=':
            return ' '
        if self.operation == '/':
            return '÷'
        if self.operation == '*':
            return '×'
        return self.operation
    
    
    def evaluate(self):
        if min(self.values)==0:
                return False
        if self.operation == '=':
            return self.values[0] == self.result
        if self.operation == '-':
            return (max(self.values)-min(self.values)) == self.result
        if self.operation == '/':            
            return (max(self.values)/min(self.values)) == self.result
        if self.operation == '+':
            return (np.sum(self.values)) == self.result
        if self.operation == '*':
            return (np.prod(self.values)) == self.result     


    def evaluate2(self):
        if min(self.values)==0:
                return False
        if self.operation == '=':
            return self.values[0]
        if self.operation == '-':
            return (max(self.values)-min(self.values))
        if self.operation == '/':            
            return (max(self.values)/min(self.values))
        if self.operation == '+':
            return (np.sum(self.values))
        if self.operation == '*':
            return (np.prod(self.values))   
        
        
class KenkenBoard:
    def __init__(self,cages):        
        self.cages = cages
        self.n = cages[0].n
        
    def __repr__(self):
        return '\n'.join(map(str,self.cages))
    
    def load_solution(self,M):
        self.solution = np.array(M)
        for cage in self.cages:
            for idx,p in enumerate(cage.points):
                cage.values[idx] = self.solution[p[0]][p[1]]
                
    def evaluate(self):
        bad_cages,bad_rows,bad_cols = [],[],[]
        self.solution = np.zeros((self.n,self.n))
        for idx,cage in enumerate(self.cages):            
            if not cage.evaluate():
                bad_cages.append(idx)
            for idx,p in enumerate(cage.points):
                self.solution[p[0]][p[1]] = cage.values[idx]
        for idx,row in enumerate(self.solution):
            if len(set(row)) != self.n:
                bad_rows.append(idx)
        for idx,col in enumerate(self.solution.T):
            if len(set(col)) != self.n:
                bad_cols.append(idx)
        return bad_cages,bad_rows,bad_cols
                
    
def parse_kenken(input_file):
    with open(input_file,'r') as f:
        lines = [l.strip() for l in f.readlines() if len(l.strip())>0]    
    cages = []
    n = int(lines[0])
    for l in lines[1:]:
        args = l.split(',')
        result=int(args[0])
        operation=args[1]
        points = []
        for a in args[2:]:
            points.append(tuple(map(int,a.strip().split(' '))))        
        cage = Cage(n=n,result=result,operation=operation,points=points)
        cages.append(cage)        
    board = KenkenBoard(cages=cages)    
    return board    


def plot_board(board,figsize=(5,5)):
    plt.close('all')
    n = board.n
    fig,ax = plt.subplots(figsize=figsize)
    for cage in board.cages:        
        squares = []
        for p in cage.points:            
            ip = p[::-1]
            squares.append(geometry.box(ip[0],ip[1],ip[0]+1,ip[1]+1))
        shape = ops.cascaded_union(squares)
        xs, ys = shape.exterior.xy        
        ax.plot(xs,ys,linewidth=3,color='black')
        ip = cage.points[0][::-1]
        ax.text(ip[0]+.1,ip[1]+.1,'%s %s'%(cage.result,cage.op_str()),ha='left',va='top')
    ax.set_xticks(range(n+1))
    ax.set_yticks(range(n+1))
    ax.tick_params(labelbottom=False,labelleft=False) 
    plt.xlim(0,n)
    plt.ylim(0,n)    
    plt.ylim(n,0)
    plt.grid(True)
    plt.show()
    
    
def plot_board_solution(board,figsize=(5,5)):
    plt.close('all')
    n = board.n
    fig,ax = plt.subplots(figsize=figsize)
    bad_cages,bad_rows,bad_cols = board.evaluate()
    for cage in board.cages:        
        squares = []
        for idx,p in enumerate(cage.points):
            ip = p[::-1]
            squares.append(geometry.box(ip[0],ip[1],ip[0]+1,ip[1]+1))
            ax.text(ip[0]+.5,ip[1]+.5,'%s'%(cage.values[idx]),ha='center',va='center',size='xx-large')
        shape = ops.cascaded_union(squares)
        xs, ys = shape.exterior.xy
        ax.fill(xs, ys, alpha=0.3, fc= 'g' if cage.evaluate() else 'r', ec='none')
        ax.plot(xs,ys,linewidth=3,color='black')
        ip = cage.points[0][::-1]
        ax.text(ip[0]+.1,ip[1]+.1,'%s %s'%(cage.result,cage.op_str()),ha='left',va='top')
    for row in bad_rows:
        shape = geometry.box(0,row+.3,0.1,row+.7)
        xs, ys = shape.exterior.xy
        ax.fill(xs, ys, alpha=1, fc='r', ec='black')
    for col in bad_cols:
        shape = geometry.box(col+.3,0,col+.7,0.1)
        xs, ys = shape.exterior.xy
        ax.fill(xs, ys, alpha=1, fc='r', ec='black')
    ax.set_xticks(range(n+1))
    ax.set_yticks(range(n+1))
    ax.tick_params(labelbottom=False,labelleft=False) 
    plt.xlim(0,n)    
    plt.ylim(n,0)
    plt.grid(True)
    plt.show()
