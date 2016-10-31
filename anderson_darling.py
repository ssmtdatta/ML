def anderson(x, dist='norm'):
    """
    Anderson-Darling test for data coming from a particular distribution
    The Anderson-Darling test is a modification of the Kolmogorov-
    Smirnov test `kstest` for the null hypothesis that a sample is
    drawn from a population that follows a particular distribution.
    For the Anderson-Darling test, the critical values depend on
    which distribution is being tested against.  This function works
    for normal, exponential, logistic, or Gumbel (Extreme Value
    Type I) distributions.
    Parameters
    ----------
    x : array_like
        array of sample data
    dist : {'norm','expon','logistic','gumbel','extreme1'}, optional
        the type of distribution to test against.  The default is 'norm'
        and 'extreme1' is a synonym for 'gumbel'
    Returns
    -------
    statistic : float
        The Anderson-Darling test statistic
    critical_values : list
        The critical values for this distribution
    significance_level : list
        The significance levels for the corresponding critical values
        in percents.  The function returns critical values for a
        differing set of significance levels depending on the
        distribution that is being tested against.
    Notes
    -----
    Critical values provided are for the following significance levels:
    normal/exponenential
        15%, 10%, 5%, 2.5%, 1%
    logistic
        25%, 10%, 5%, 2.5%, 1%, 0.5%
    Gumbel
        25%, 10%, 5%, 2.5%, 1%
    If A2 is larger than these critical values then for the corresponding
    significance level, the null hypothesis that the data come from the
    chosen distribution can be rejected.
    References
    ----------
    .. [1] http://www.itl.nist.gov/div898/handbook/prc/section2/prc213.htm
    .. [2] Stephens, M. A. (1974). EDF Statistics for Goodness of Fit and
           Some Comparisons, Journal of the American Statistical Association,
           Vol. 69, pp. 730-737.
    .. [3] Stephens, M. A. (1976). Asymptotic Results for Goodness-of-Fit
           Statistics with Unknown Parameters, Annals of Statistics, Vol. 4,
           pp. 357-369.
    .. [4] Stephens, M. A. (1977). Goodness of Fit for the Extreme Value
           Distribution, Biometrika, Vol. 64, pp. 583-588.
    .. [5] Stephens, M. A. (1977). Goodness of Fit with Special Reference
           to Tests for Exponentiality , Technical Report No. 262,
           Department of Statistics, Stanford University, Stanford, CA.
    .. [6] Stephens, M. A. (1979). Tests of Fit for the Logistic Distribution
           Based on the Empirical Distribution Function, Biometrika, Vol. 66,
           pp. 591-595.
    """
    if dist not in ['norm', 'expon', 'gumbel', 'extreme1', 'logistic']:
        raise ValueError("Invalid distribution; dist must be 'norm', "
                         "'expon', 'gumbel', 'extreme1' or 'logistic'.")
    y = sort(x)
    xbar = np.mean(x, axis=0)
    N = len(y)
    if dist == 'norm':
        s = np.std(x, ddof=1, axis=0)
        w = (y - xbar) / s
        z = distributions.norm.cdf(w)
        sig = array([15, 10, 5, 2.5, 1])
        critical = around(_Avals_norm / (1.0 + 4.0/N - 25.0/N/N), 3)
    elif dist == 'expon':
        w = y / xbar
        z = distributions.expon.cdf(w)
        sig = array([15, 10, 5, 2.5, 1])
        critical = around(_Avals_expon / (1.0 + 0.6/N), 3)
    elif dist == 'logistic':
        def rootfunc(ab, xj, N):
            a, b = ab
            tmp = (xj - a) / b
            tmp2 = exp(tmp)
            val = [np.sum(1.0/(1+tmp2), axis=0) - 0.5*N,
                   np.sum(tmp*(1.0-tmp2)/(1+tmp2), axis=0) + N]
            return array(val)

        sol0 = array([xbar, np.std(x, ddof=1, axis=0)])
        sol = optimize.fsolve(rootfunc, sol0, args=(x, N), xtol=1e-5)
        w = (y - sol[0]) / sol[1]
        z = distributions.logistic.cdf(w)
        sig = array([25, 10, 5, 2.5, 1, 0.5])
        critical = around(_Avals_logistic / (1.0 + 0.25/N), 3)
    else:  # (dist == 'gumbel') or (dist == 'extreme1'):
        xbar, s = distributions.gumbel_l.fit(x)
        w = (y - xbar) / s
        z = distributions.gumbel_l.cdf(w)
        sig = array([25, 10, 5, 2.5, 1])
        critical = around(_Avals_gumbel / (1.0 + 0.2/sqrt(N)), 3)

    i = arange(1, N + 1)
    A2 = -N - np.sum((2*i - 1.0) / N * (log(z) + log(1 - z[::-1])), axis=0)

    return AndersonResult(A2, critical, sig)