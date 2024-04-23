import os
import sys
import random
import pygame as pg
import time


WIDTH, HEIGHT = 1600, 900
DELTA = { #移動量辞書(押下キー:移動タプル)
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0)
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct:pg.Rect) -> tuple[bool,bool]:
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate =False
    return yoko, tate
'''
def drawract():
    screen = pg.display.set_mode((1600,900))
    rect = pg.Surface((0,0))
    Draw_rect = pg.draw.ract(rect,(0,0,0),(10,10),10)
'''
def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    #ここからこうかとんの設定
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    
    #ここから爆弾の設定
    bd_img = pg.Surface((20,20))
    bd_img.set_colorkey((0,0,0))
    pg.draw.circle(bd_img,(255,0,0),(10,10),10)
    bd_rct = bd_img.get_rect()
    bd_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5,+5 #横方向速度、縦方向速度
    def drawract():
        shikaku = pg.Surface((WIDTH,HEIGHT))
        pg.draw.rect(shikaku,(0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
        shikaku.set_alpha(200)
        screen.blit(shikaku,(0,0))
        fonto = pg.font.Font(None,80)
        txt = fonto.render("Game Over",True,(255,255,255))
        screen.blit(txt,[WIDTH/2,HEIGHT/2])   
        kn_img = pg.image.load("fig/8.png")
        screen.blit(kn_img,[900,600])
        pg.display.update()
        time.sleep(5)
        return
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bd_rct):
            drawract()
            print("Game Over")
            break

        screen.blit(bg_img, [0, 0]) 

        #こうかとんの移動と表示
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)

        #爆弾の移動と表示
        bd_rct.move_ip(vx, vy)
        screen.blit(bd_img, bd_rct)
        yoko, tate = check_bound(bd_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
