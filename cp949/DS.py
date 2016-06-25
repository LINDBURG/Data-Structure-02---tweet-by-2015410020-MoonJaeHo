WHITE = 0
GRAY = 1
BLACK = 2

class Adj:
    def __init__(self):
        self.n = 0
        self.next = None

class Vertex(object):
    def __init__(self):
        self.color = WHITE
        self.parent = -1
        self.uid = '(none)'
        self.regdat = '(none)'
        self.nick = '(none)'
        self.fnumber = 0
        self.friend = []
        self.tnumber = 0
        self.tweet = []
        self.tdat = []
        self.first = None
    def add(self, v):
        a = Adj()
        a.n = v.n
        a.next = self.first
        self.first = a

class BFSVertex(Vertex):
    def __init__(self):
        super(BFSVertex, self).__init__()
        self.d = 1E10    #infty

class Queue:
    def __init__(self):
        self.front = 0
        self.rear = 0
        self.sz = 0
        self.buf = []
    def create_queue(self,sz):
        self.sz = sz
        self.buf = list(range(sz))  # malloc(sizeof(int)*sz)
    def enqueue(self,val):
        self.buf[self.rear] = val
        self.rear = (self.rear + 1) % self.sz
    def dequeue(self):
        res = self.buf[self.front]
        self.front = (self.front + 1) % self.sz
        return res
    def is_empty(self):
        return self.front == self.rear

def bfs(vertices, s):
    for u in vertices:
        if u.n != s.n:
            u.color = WHITE
            u.d = 1E10
            u.parent = -1
    s.color = GRAY
    s.d = 0
    s.parent = -1
    q = Queue()
    q.create_queue(len(vertices))
    q.enqueue(s.n)        # enquque node number
    while not q.is_empty():
        u = q.dequeue()   # node number
        adj_v = vertices[u].first
        while adj_v:
            if vertices[adj_v.n].color == WHITE:
                vertices[adj_v.n].color = GRAY   # gray
                vertices[adj_v.n].d = vertices[u].d + 1
                vertices[adj_v.n].parent = u
                q.enqueue(adj_v.n)
            adj_v = adj_v.next
        vertices[u].color = BLACK           # black

def transpose(vertices):
    a = [None, None, None, None, None, None, None, None]
    for u in vertices:
        v = u.first
        while v:
            temp = Adj()
            temp.n = u.n
            temp.next = a[v.n]
            a[v.n] = temp
            v = v.next
    for u in vertices:
        u.first = a[u.n]
        
def print_vertex(vertices,n):
    print (vertices[n].uid, end=' ')
    print (vertices[n].color, end=' ')
    print (vertices[n].parent, end=' ')
    print (vertices[n].d, end=':')
    p = vertices[n].first
    while p:
        print (vertices[p.n].uid, end = ' ')
        p = p.next
    print('')

def  readDF():
    global unumber,frecord,tweet,Account,vertices, tnumber,tweets,tweetBy,tweetTime
    unumber =0
    frecord = 0
    tnumber = 0
    Account = []
    vertices = []
    tweets = []
    tweetBy = []
    tweetTime = []
    
    f = open("user.txt", 'r')
    while True:
        uid = f.readline()
        if not uid: break
        regdat = f.readline()
        if not regdat: break
        nick = f.readline()
        if not nick: break
        f.readline()
        Account.append(BFSVertex())
        vertices.append(Account[unumber])
        Account[unumber].uid = uid
        Account[unumber].regdat = regdat
        Account[unumber].nick = nick
        unumber = unumber + 1
    print("Total users : %d" % unumber)
    f.close()
    
    f = open("friend.txt", 'r')
    while True:
        uid = f.readline()
        if not uid: break
        fid = f.readline()
        if not fid: break
        f.readline()
        for i in range(0,len(Account)):
            if Account[i].uid ==uid:
                Account[i].friend = fid
                Account[i].fnumber = Account[i].fnumber + 1
                frecord =  frecord + 1
                break
    print("Total friendship records : %d" % frecord)
    f.close()
    
    f= open("word.txt",'r')
    while True:
        uid = f.readline()
        if not uid: break
        tdat = f.readline()
        if not tdat: break
        tweet = f.readline()
        if not tweet: break
        f.readline()
        for i in range(0,len(Account)):
            if Account[i].uid==uid:
                Account[i].tweet = tweet
                Account[i].tdat = tdat
                Account[i].tnumber = Account[i].tnumber + 1
                tnumber = tnumber + 1
                flag =0
                for k in range(0,len(tweets)):
                    if tweets[k] == tweet:
                        tweetTime[k] = tweetTime[k] + 1
                        flag = 1
                        break
                if flag == 0:
                    tweets.append(tweet)
                    tweetBy.append(uid)
                    tweetTime.append(0)
                break
    print("Total tweets : %d" % tnumber)
    f.close()


        
def statistic():
    print("Average number of friends : %d" % (frecord/unumber))
    minfriend = Account[0].fnumber
    maxfriend = Account[0].fnumber
    mintweet = Account[0].tnumber
    maxtweet = Account[0].tnumber
    for i in range(0,len(Account)):
        if minfriend>Account[i].fnumber:
           minfriend = Account[i].fnumber
        elif maxfriend < Account[i].fnumber:
            maxfriend  = Account[i].fnumber
        if mintweet>Account[i].tnumber:
           mintweet = Account[i].tnumber
        elif maxtweet < Account[i].tnumber:
            maxtweet = Account[i].tnumber
    print("Minimum friends : %d" % minfriend)
    print("Maximum number of friends : %d\n" % maxfriend)
    print("Average tweets per user : %d" % (tnumber/unumber))
    print("Minium tweets per user : %d" % mintweet)
    print("Maximu tweets per user : %d" % maxtweet)
    
def mostW():
    word = []
    for i in range(0,5):
        if tweetTime[i]<=tweetTime[0] and tweetTime[i]<=tweetTime[1] and tweetTime[i]<=tweetTime[2] and tweetTime[i]<=tweetTime[3] and tweetTime[i]<=tweetTime[4]:
            word = [i,i,i,i,i]
            break
    for i in range(0,len(tweets)):
        if tweetTime[i] > tweetTime[word[4]]:
            if tweetTime[i] > tweetTime[word[0]]:
                word[0] = i
            elif tweetTime[i] > tweetTime[word[1]]:
                word[1] = i
            elif tweetTime[i] > tweetTime[word[2]]:
                word[2] = i
            elif tweetTime[i] > tweetTime[word[3]]:
                word[3] = i
            else:
                word[4] = i
    print("Top 5 most tweeted words\n")
    for i in range(0,5):
        print("%d위 : %s    %d회" %(i+1, tweets[word[i]], tweetTime[word[i]]))
        
def mostU():
    word = []
    for i in range(0,5):
        if Account[i].tnumber <=Account[0].tnumber and Account[i].tnumber <=Account[1].tnumber and Account[i].tnumber <=Account[2].tnumber and Account[i].tnumber <=Account[3].tnumber and Account[i].tnumber <=Account[4].tnumber:
            word = [i,i,i,i,i]
            break
    for i in range(0,len(Account)):
        if Account[i].tnumber > Account[word[4]].tnumber:
            if Account[i].tnumber > Account[word[0]].tnumber:
                word[0] = i
            elif Account[i].tnumber > Account[word[1]].tnumber:
                word[1] = i
            elif Account[i].tnumber > Account[word[2]].tnumber:
                word[2] = i
            elif Account[i].tnumber > Account[word[3]].tnumber:
                word[3] = i
            else:
                word[4] = i
    print("Top 5 most tweeted users\n")
    for i in range(0,5):
        print("%d위 : %s  %s  %d회" %(i+1,Account[word[i]].uid, Account[word[i]].nick,Account[word[i]].tnumber))
    
def findU():
    userfind = []
    word = input("찾으시려는 유저의 트윗을 입력해 주세요")
    for i in range(0,len(tweets)):
        if str(tweets[i]) == word:
             userfind.append(tweetBy[i])
             rec = i
    print("검색된 유저id :\n")
    for i in range(0,len(userfind)):
        print(userfind[i])
    
def findRecent():
    userfriend = []
    for i in range(0,len(Account)):
        for k in range(0,len(Account[i].friend)):
            if Account[i].friend[k] == Account[rec].uid:
                userfriend.append(Account[i].nick)
    print("최근 검색 유저의 친구")
    for i in range(0,len(userfriend)):
        print(userfriend[i])
        
def deleteMW():
    word = input("제거하시려는 트윗을 입력해 주세요")
    for i in range(0,len(tweets)):
        if tweets[i] ==word:
            del tweets[i]
            del tweetBy[i]
            del tweetTime[i]
            break
    for i in range(0,len(Account)):
        for k in range(0,len(Account[i].tweet)):
            if Account[i].tweet[k] == word:
                del Account[i].tweet[k]
                Account[i].tnumber = Account[i].tnumber - 1
                tnumber = tnumber - 1
    
def deleteUMW():
    word = input("제거하시려는 유저가 한 트윗을 입력해 주세요")
    for i in range(0,len(tweets)):
        if tweets[i] ==word:
            del tweets[i]
            del tweetBy[i]
            del tweetTime[i]
            break
    for i in range(0,len(Account)):
        for k in range(0,len(Account[i].tweet)):
            if Account[i].tweet[k] == word:
                del Account[i]
            """지금까지 짠 코드 상태상 유저 안에 들어가 있는 모든 항목들을 일일히 검사해
연결관계를 일일히 삭제해야 하지만 시간복잡도가 너무 높아지므로 생략합니다 ㅠ

"""
                
def SCC():
    print("미구현")

def shortest():
    print("asdf")
    
def main():
    global rec
    ext=0
    rec =0
    print("------------------START---------------")
    while not ext:
        print("0. Read data files\n")
        print("1. display statistics\n")
        print("2. Top 5 most tweeted words\n")
        print("3. Top 5 most tweeted users\n")
        print("4. Find users who tweeted a word (e.g., ’연세대’)\n")
        print("5. Find all people who are friends of the above users\n")
        print("6. Delete all mentions of a word\n")
        print("7. Delete all users who mentioned a word\n")
        print("8. Find strongly connected components\n")
        print("9. Find shortest path from a given user\n")
        print("99. Quit \n")
        try:
            select = int(input("SELECT MENU : "))
        except:
            print("숫자를 입력해 주세요")
        else:
            try:
                if(select==0):
                        readDF()
                if unumber>0:
                    if(select==1):
                        statistic()
                    elif(select==2):
                        mostW()
                    elif(select==3):
                        mostU()
                    elif(select==4):
                        findU()
                    elif(select==5):
                        if rec!=0:
                            findRecent()
                        else:
                            print("최근 검색한 user가 없습니다.")
                    elif(select==6):
                        deleteMW()
                    elif(select==7):
                        deleteUMW()
                    elif(select==8):
                        SCC()
                    elif(select==9):
                        shortest()
                    elif(select==99):
                        exit()
                    else:
                        print("적절한 숫자를 입력해 주세요")
                print("############################\n")
            except:
                print("0번을 먼저 진행해 주세요")

main()
