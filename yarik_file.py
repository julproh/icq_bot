# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Вяглядит пока как дерьмо, зато работает само))))

# %%
import threading
import pandas
import urllib.request
import schedule
import time
import ssl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt
from scipy.optimize import curve_fit
import matplotlib.ticker as ticker


# %%
def downloading():
    print('Beginning file download with urllib2...')
    ssl._create_default_https_context = ssl._create_unverified_context
    url = 'https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.xlsx'
    urllib.request.urlretrieve(url, 'covid_data.xlsx')

def run_threaded(downloading):
    job_thread = threading.Thread(target=downloading, daemon = True)
    job_thread.start()

schedule.every().day.at("11:31").do(run_threaded, downloading)


#я чекнул, на сайте обновляется ,каждый день в 11:30, мы будем в 11:31


# %%
print('Beginning file download with urllib2...')
url = 'https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.xlsx'
ssl._create_default_https_context = ssl._create_unverified_context
urllib.request.urlretrieve(url, 'covid_data.xlsx')

# это для теста, забей


# %%
data = pandas.read_excel('covid_data.xlsx')
data.head()

#считываем данные


# %%
data['date'] = pandas.to_datetime(data['date'])
data['date']

#преобразуем даты к божескому виду

# %% [markdown]
# # Вот здесь надо ввести название страны и все сделается само

# %%
print('Введи страну сучка, например, Russia or Urkain, Germany. Вводи так как написано в примере, пидарас, иначе наебнется все')
print('Вводи по английский с большой буквы, умник')
country = input()
date_interval = 5 #интервал для графика, забей, не трогай


# %%
# для поиска нужной страны в списке
def get_coordinates(country):
    amount = 0
    for i in range(len(data)):
        if data.iloc[i,1] == country:
            amount += 1
            if amount == 1:
                start = i
            end = start + amount
        else:
            pass
    return [start, end, amount]


# %%
# Получили координаты страны : индекс начала, индекс конца и длинна этого списка
coordinates = get_coordinates(country)
coordinates


# %%
start = coordinates[0]
end = coordinates[1]
amount = coordinates[2]


# %%
# функция апроксимации
def f(x, a, b, c):
    return np.exp(a*x + b) + c


# %%
# Определили списки количества зараженных
Infected = np.array(data['total_cases'].iloc[start:end])
days = np.arange(1,amount+1)


# %%
# Отсеиваем хламную информацию, будем строить минимум от 100 заболевших
def find_new_start(Infected):
    Infected_2 = []
    n = 0
    for i in range(len(Infected)):
        if Infected[i] > 100:
            n += 1
            if n == 1:
                start_new = i
            Infected_2.append(Infected[i])
    Infected_2 = np.array(Infected_2)
    return (Infected_2, start_new)


# %%
start_new = find_new_start(Infected)[1]
Infected_2 = find_new_start(Infected)[0]
days1 = np.arange(1,amount-start_new+1)


# %%
#Апроксимация


#коэффициенты
beta_opt1, beta_cov1 = curve_fit(f, days1, Infected_2)
a = beta_opt1[0]
b = beta_opt1[1]
c = beta_opt1[2]

print('a = ', a)
print('b = ', b)
print('c = ', c)


#получим погрешности для коэффициентов
sigma_a = np.sqrt(beta_cov1[0,0])
sigma_b = np.sqrt(beta_cov1[1,1])
sigma_c = np.sqrt(beta_cov1[2,2])

print('sigma_a = ', sigma_a)
print('sigma_b = ', sigma_b)
print('sigma_c = ', sigma_c)


residuals1 = Infected_2 - f(days1,*beta_opt1)
fres1 = sum(residuals1**2)
Stand_error = np.sqrt(fres1/len(days1))
print('Stand_error = ', Stand_error)

print('Relative S_r a = % ', 100* sigma_a/a)
print('Relative S_r b = % ', 100* sigma_b/abs(b))
print('Relative S_r c = % ', 100* sigma_c/abs(c))


# %%
fig, ax = plt.subplots(figsize=(15, 12))

past = min(data['date'].iloc[start+start_new:end])
now = max(data['date'].iloc[start+start_new:end]) + dt.timedelta(days=1)
days2 = mdates.drange(past,now,dt.timedelta(days=1))


delta = days2[0] - 1
beta_opt2 = np.array([a,b-delta * a,c])



ax.plot(days2, f(days2, *beta_opt2), 'coral', lw=2)
#ax.plot(days2, Infected, 'coral', lw=2)
#ax.scatter(days2, Infected, s = 1, c = 'red')
lgnd = ax.legend(['We gonna chill ~(˘▾˘~) with error $\pm$ %d people' % Stand_error ], loc='upper left', shadow=True)

ax.set_title('Infected in %s (date)      from %s to %s' % (country, min(data['date'].iloc[start+start_new:end]).strftime("%d.%m"), max(data['date'].iloc[start+start_new:end]).strftime("%d.%m")))
ax.set_ylabel('Infected')
ax.set_xlabel('Date (day.month)')

ax.grid(which='major',
        color = 'k')

ax.minorticks_on()

ax.grid(which='minor',
        color = 'gray',
        linestyle = ':', linewidth = 0.5)

ax.grid(which='major', linewidth = 0.5)


plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=date_interval))
plt.errorbar(days2, Infected_2, fmt = 'ro', markersize = '2', yerr = Stand_error, capsize = 2, elinewidth = 2, capthick = 1, ecolor = 'violet')
plt.gcf().autofmt_xdate()
plt.savefig('infected2.pdf')
plt.show()


# %%
# я пытаюсь построить гистограмму, выглядит пока как дерьмо ,зато работает само ))))

fig, ax = plt.subplots()

ax.bar(data['date'].iloc[start+start_new:end], Infected_2)

ax.set_facecolor('seashell')
fig.set_facecolor('floralwhite')
fig.set_figwidth(12)    
fig.set_figheight(6)    
plt.savefig('infected_hist.pdf')
plt.show()


# %%



# %%


